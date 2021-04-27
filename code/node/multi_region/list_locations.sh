#!/bin/bash

# Use the Azure CLI to get the list of regions your
# subscription has access to.

az account list-locations > locations.json

cat locations.json | grep name | sort
