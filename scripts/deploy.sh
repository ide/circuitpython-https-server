#!/usr/bin/env bash

set -euo pipefail

script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_directory="$script_directory/.."

if ! command -v rsync &> /dev/null; then
  echo 'rsync is not installed on this computer. rsync is used to copy the application code to your device. Install it using the package manager you use with your OS.'
  exit 1
fi

if ! command -v circup &> /dev/null; then
  echo 'circup is not installed on this computer. circup is used to install CircuitPython dependencies on your device. Install it by following the instructions in the circup repository at: https://github.com/adafruit/circup'
  exit 1
fi

echo 'Detecting your CircuitPython device...'
device_path=$(python3 -c 'import circup; print(circup.find_device())')
if [ "$device_path" == 'None' ]; then
  echo 'circup could not detect a connected CircuitPython device. Make sure your device is flashed with CircuitPython and connected to your computer with a USB data cable.'
  exit 1
fi
echo "Found device at $device_path"

echo 'Copying application code...'
rsync --verbose --recursive --delete --checksum --times --modify-window=1 \
  --include '/._*' --exclude '/.*' \
  --exclude '/boot_out.txt' --exclude '/settings.toml' --exclude '/lib' \
  "$project_directory/src/" "$device_path"
echo 'Finished copying application code'

echo 'Installing libraries with circup'
circup install --all
echo 'Finished installing libraries with circup'
