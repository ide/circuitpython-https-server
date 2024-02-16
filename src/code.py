import os
import ssl
import time
import traceback

import socketpool
import supervisor
import wifi

from adafruit_httpserver.server import Server as HTTPServer
from adafruit_httpserver.response import Response


def index(request):
    u = os.uname()
    return Response(
        request,
        content_type="text/plain",
        body=f"Hello from {u.machine} running {u.version}!\n",
    )


def main() -> None:
    print("Connecting to the local Wi-Fi network...")
    wifi.radio.hostname = "picow"
    wifi.radio.connect(
        os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD")
    )
    print("Connected to the local network")
    print(f"  IP address = {wifi.radio.ipv4_address}")
    print(f"  Router     = {wifi.radio.ipv4_gateway}")
    print(f"  DNS server = {wifi.radio.ipv4_dns}")

    host = str(wifi.radio.ipv4_address)
    pool = socketpool.SocketPool(wifi.radio)
    http_server = HTTPServer(pool)
    http_server.route("/")(index)
    http_server.start(host, port=80)

    ssl_context = ssl.create_default_context()
    # The Pico is the server and does not require a certificate from the client, so disable
    # certificate validation by explicitly specifying no verification CAs
    ssl_context.load_verify_locations(cadata="")
    ssl_context.load_cert_chain(
        "certificates/certificate-chain.pem", "certificates/key.pem"
    )
    tls_pool = TLSServerSocketPool(pool, ssl_context)
    https_server = HTTPServer(tls_pool)
    https_server.route("/")(index)
    https_server.start(host, port=443)

    print()
    print("The web server is listening on:")
    print(f"  http://{host}")
    print(f"  https://{host}")
    print(f"  http://{wifi.radio.hostname}.local")
    print(f"  https://{wifi.radio.hostname}.local")
    print()

    while True:
        http_server.poll()
        try:
            https_server.poll()
        except OSError as error:
            if error.strerror.startswith("MBEDTLS_ERR_"):
                print(f"TLS library error {error.strerror} with code {error.errno}")
            else:
                raise


class TLSServerSocketPool:
    def __init__(self, pool, ssl_context):
        self._pool = pool
        self._ssl_context = ssl_context

    @property
    def AF_INET(self):
        return self._pool.AF_INET

    @property
    def SOCK_STREAM(self):
        return self._pool.SOCK_STREAM

    def socket(self, *args, **kwargs):
        socket = self._pool.socket(*args, **kwargs)
        return self._ssl_context.wrap_socket(socket, server_side=True)

    def getaddrinfo(self, *args, **kwargs):
        return self._pool.getaddrinfo(*args, **kwargs)


try:
    main()
except Exception as exception:
    print("".join(traceback.format_exception(exception, limit=8)))
    print("Reloading in 3 seconds...")
    time.sleep(3)
    supervisor.reload()
