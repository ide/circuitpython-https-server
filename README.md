# CircuitPython HTTPS Web Server (for Raspberry Pi Pico W)

> Note: this example isn't complete! There is an issue with the TLS library, perhaps an incompatible certificate. Help investigating is appreciated!

This is an example of an HTTPS web server written in [CircuitPython](https://circuitpython.org/), intended to run on a [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#raspberry-pi-pico-w-and-pico-wh). [Adafruit](https://www.adafruit.com/) (the makers of CircuitPython) and the CircuitPython documentation have [guides](https://learn.adafruit.com/pico-w-http-server-with-circuitpython/code-the-pico-w-http-server) on running an unsecured HTTP server but none on serving content over HTTPS. This example will show you how to run an HTTPS server from a Pico W.

## Why HTTPS for Pico W? (A better user experience for IoT web apps)

In the context of a Pico W serving content to your local network, the main motivation for HTTPS is to enable [web browser features limited to secure contexts](https://developer.mozilla.org/en-US/docs/Web/Security/Secure_Contexts/features_restricted_to_secure_contexts). These include [Service Workers](https://developer.mozilla.org/en-US/docs/Web/API/Service_Worker_API), which are needed to implement websites that work offline or use push notifications, two common features you might want in an IoT application.

Imagine you're at home and you visit your Pico W's homepage from your web browser. You add the web app to your home screen and your phone presents the web app somewhat like a native app with a home screen icon and its own entry in the task switcher. The web app lets you subscribe to push notifications from your Pico that you'll receive even when you're away from home. And, the web app also loads in "offline" mode when you're away from home and can't connect to your Pico. This is what the user experience should be like for web-based IoT applications.

The secondary motivation for HTTPS is security. The threat model of your Pico W accessed from your local network is different from a web server accessed from the internet. Your Pico W is already protected by your router and only trusted devices with your Wi-Fi password or physical Ethernet connections can access it. However, defense in depth is a good security principle and HTTPS prevents even your trusted devices from sniffing or tampering with traffic to your Pico W.

## Goals and non-goals

The main goal of this repository is to show how to set up a web server that serves content over HTTPS and runs with CircuitPython on a Raspberry Pi Pico W. It's intended for a small, private home network. It uses self-signed certificates and requires installing the CA certificate on client devices. 

There are also several non-goals of this repository, which help keep its scope small. The example server targets only the Pico W and not other boards that CircuitPython supports, though it might happen to work for them, too. C
4096-bit



