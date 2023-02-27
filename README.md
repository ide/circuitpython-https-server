# CircuitPython HTTPS Web Server (for Raspberry Pi Pico W)

This is an example of an HTTPS web server written in [CircuitPython](https://circuitpython.org/), intended to run on a [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#raspberry-pi-pico-w-and-pico-wh). [Adafruit](https://www.adafruit.com/) (the makers of CircuitPython) and the CircuitPython documentation have [guides](https://learn.adafruit.com/pico-w-http-server-with-circuitpython/code-the-pico-w-http-server) on running an unsecured HTTP server but none on serving content over HTTPS. This example will show you how to run an HTTPS server from a Pico W.

Note: the server is very slow and takes about 6 seconds to respond with a tiny HTML file over HTTPS. In comparison, responding with the same file over HTTP takes 75 to 350 milliseconds.

## Getting started

1. Follow [Adafruit's guide to connecting your Pico W to Wi-Fi](https://learn.adafruit.com/pico-w-wifi-with-circuitpython/overview). Make sure you can run the the basic Wi-Fi test successfully.

2. Clone this repository to your computer: `git clone https://github.com/ide/circuitpython-https-server.git`

3. Copy the contents of the **src** directory to your **CIRCUITPY** volume. On macOS, you can run `scripts/deploy.sh` if you have [`rsync`](https://formulae.brew.sh/formula/rsync) and [`circup`](https://github.com/adafruit/circup) installed. Make sure your **settings.toml** file on your Pico still has your Wi-Fi credentials you configured when following Adafruit's Wi-Fi guide. 

4. Connect to your Pico W's serial console. See [Adafruit's guide](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console) on how to do this. On macOS you can run `scripts/repl.sh`. Reload the code running in CircuitPython by entering Ctrl-C in the console.

5. The program running on your Pico W will start a web server and print two URLs, one with the Pico W's local IP address (e.g. https://192.168.1.2) and one with its local mDNS hostname (configured to be https://picow.local).

6. Run `curl --insecure https://picow.local` (or specify your Pico W's IP address). After about 10 seconds, you should see a small HTML response.

## Why HTTPS for Pico W? (A better user experience for IoT web apps)

In the context of a Pico W serving content to your local network, the main motivation for HTTPS is to enable [web browser features limited to secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts/features_restricted_to_secure_contexts). These include [Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API), which are needed to implement websites that work offline or use push notifications, two common features you might want in an IoT application.

Imagine you're at home and you visit your Pico W's homepage from your web browser. You add the web app to your home screen and your phone presents the web app somewhat like a native app with a home screen icon and its own entry in the task switcher. The web app lets you subscribe to push notifications from your Pico that you'll receive even when you're away from home. And, the web app also loads in "offline" mode when you're away from home and can't connect to your Pico. This is what the user experience should be like for private, web-based IoT applications.

The secondary motivation for HTTPS is security. The threat model of your Pico W accessed from your local network is different from that of a web server accessed from the internet. Your Pico W is already protected by your router and only trusted devices with your Wi-Fi password or physical Ethernet connections can access it. However, defense in depth is a good security principle and HTTPS prevents even your trusted devices from sniffing or tampering with traffic to your Pico W.

## Goals and non-goals

The main goal of this repository is to show how to set up a web server that serves content over HTTPS and runs with CircuitPython on a Raspberry Pi Pico W. It's intended for a small, private home network. It uses self-signed certificates and requires installing the CA certificate on client devices.

There are also several non-goals of this repository, which help keep its scope small. The repository provides an example, not a Python package. If support for serving content over HTTPS with CircuitPython is actually important, it probably makes sense for Adafruit to steer developers towards a package they provide. The example server targets only the Pico W and not other boards that CircuitPython supports, though it might happen to work for them, too. 

## Things to be aware of

This example uses a 1024-bit RSA certificate for performance. With a 1024-bit certificate, the server responds in about 6 seconds, while a 2048-bit certificate causes it to take about 9 seconds. However, 1024-bit certificates are considered cryptographically insecure. This said, the primary motivation of this project is to enable web browser APIs that require HTTPS on Pico W devices running in a private, local network that is already protected.


