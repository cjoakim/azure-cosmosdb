#!/bin/bash

# see https://docs.microsoft.com/en-us/azure/cosmos-db/linux-emulator?tabs=ssl-netstd21

ipaddr="`ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}' | head -n 1`"

echo $ipaddr

curl -k https://$ipaddr:8081/_explorer/emulator.pem > emulatorcert.crt

cat emulatorcert.crt

# Open the Keychain Access app on your Mac to import the emulator certificate.
# Select File and Import Items and import the emulatorcert.crt.
# change the trust settings to Always Trust.

