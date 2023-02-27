#!/usr/bin/env bash

set -euo pipefail

script_directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Derived from https://www.linode.com/docs/guides/create-a-self-signed-tls-certificate/
openssl req -new -newkey rsa:1024 -x509 -sha256 -days 365 -nodes \
  -subj '/CN=picow.local' \
  -out "$script_directory/../src/certificates/certificate-chain.pem" \
  -keyout "$script_directory/../src/certificates/key.pem"
