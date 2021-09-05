#!/bin/bash

# see https://docs.microsoft.com/en-us/azure/cosmos-db/linux-emulator?tabs=ssl-netstd21
# https://localhost:8081/_explorer/index.html

ipaddr="`ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}' | head -n 1`"

echo $ipaddr

docker pull mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator

docker run \
    -p 8081:8081 \
    -p 10251:10251 \
    -p 10252:10252 \
    -p 10253:10253 \
    -p 10254:10254 \
    -m 3g \
    --cpus=2.0 \
    --name=test-linux-emulator \
    -e AZURE_COSMOS_EMULATOR_PARTITION_COUNT=10 \
    -e AZURE_COSMOS_EMULATOR_ENABLE_DATA_PERSISTENCE=true \
    -e AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=$ipaddr \
    -it mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator

# docker pull mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator
# docker run -p 8081:8081 -p 10251:10251 -p 10252:10252 -p 10253:10253 -p 10254:10254  -m 3g --cpus=2.0 --name=test-linux-emulator -e AZURE_COSMOS_EMULATOR_PARTITION_COUNT=10 -e AZURE_COSMOS_EMULATOR_ENABLE_DATA_PERSISTENCE=true -e AZURE_COSMOS_EMULATOR_IP_ADDRESS_OVERRIDE=$ipaddr -it mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator

# $ docker ps
# CONTAINER ID   IMAGE                                                    COMMAND                  CREATED          STATUS          PORTS                                                                                                              NAMES
# 4121c31837f9   mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator   "/usr/local/bin/cosm…"   19 minutes ago   Up 19 minutes   0.0.0.0:8081->8081/tcp, :::8081->8081/tcp, 0.0.0.0:10251-10254->10251-10254/tcp, :::10251-10254->10251-10254/tcp   test-linux-emulator

# (tech) [~/github/cj-tech]$ docker stop 4121c31837f9
# 4121c31837f9

# (tech) [~/github/cj-tech]$ docker ps
# CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

# curl -k https://$ipaddr:8081/_explorer/emulator.pem > emulatorcert.crt