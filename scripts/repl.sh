#!/usr/bin/env bash

set -euo pipefail

device=$(ls -1 -t /dev/tty.usbmodem*)

# Reattach to an existing session if one exists; otherwise create a new one
screen -D -R -S circuitpython "$device" 115200
