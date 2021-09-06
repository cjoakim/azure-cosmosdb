# CosmosDB Emulator

## Links

- https://docs.microsoft.com/en-us/azure/cosmos-db/linux-emulator?tabs=ssl-netstd21

## Docker Image

```
$ docker pull mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator
```

## Start the Container

```
$ ipaddr="`ifconfig | grep "inet " | grep -Fv 127.0.0.1 | awk '{print $2}' | head -n 1`"

$ docker run \
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
```

See shell script [cosmos_emulator.sh](cosmos_emulator.sh)

### Get and install the certificate

```
$ curl -k https://$ipaddr:8081/_explorer/emulator.pem > emulatorcert.crt
```

See https://docs.microsoft.com/en-us/azure/cosmos-db/linux-emulator?tabs=ssl-netstd21

## Web UI

- Visit https://localhost:8081/_explorer/index.html

<p align="center"><img src="../presentations/img/emulator-on-macos.png" width="80%"></p>

## Environment Variables

I use the following environment variables in my code for emulator configuration:

```
AZURE_COSMOSDB_EMULATOR_ACCT=localhost:8081
AZURE_COSMOSDB_EMULATOR_KEY=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==
AZURE_COSMOSDB_EMULATOR_URI=https://localhost:8081/
```
