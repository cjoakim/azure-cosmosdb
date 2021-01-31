# azure-cosmosdb

A collection of CosmosDB related [code](code/), [links](links.md), and [presentations](presentations/).

## CosmosDB

<p align="center"><img src="presentations/img/azure-cosmos-db-gray.png" width="95%"></p>

---

## Directory Structure of this Repo


```
    Directory                Status
    ---------                ------

├── automation               Azure ARM and az CLI deployment scripts
│   ├── arm                  todo
│   └── az                   implemented
├── code                     CosmosDB SDK programming examples in each language
│   ├── dotnet               implemented
│   ├── java                 implemented
│   ├── java_spring          todo
│   ├── node                 todo
│   └── python               implemented
├── data                     Common data files used across this repo
│   ├── airports
│   ├── amtrak
│   ├── graph
│   │   ├── amtrak  
│   │       ├── gremlin               
│   │   └── bom              
│   │       ├── gremlin      
│   │       └── libs         
│   └── postal               
├── dbs                      CosmosDB DBMS-Specific files
│   ├── cassandra
│   ├── graph
│   └── mongo                implemented
├── docs
├── functions                implemented
├── live_data_migrator       todo
├── notebooks                todo
├── presentations            wip
├── server_side              Stored Prodedures, Triggers, UDF examples in js/ directory
└── synapse_pyspark          todo
```

This repo is a **work in progress; not all of the above are implemented at this time**.

## Environment Variables used in this Repo

I use system environment variables for all configuration in this repository;
never use hard-coded values in your code and source-controlled files.

These environment variable names are **my personal conventions, and not required by Azure CosmosDB**.

```
AZURE_SUBSCRIPTION_ID                <-- Your Azure Subscription ID
AZURE_COSMOSDB_DATA_DIR              <-- Set this to the location of the data/ directory of this (cloned) repo.

AZURE_COSMOSDB_CASSANDRA_ACCT
AZURE_COSMOSDB_CASSANDRA_CERTFILE
AZURE_COSMOSDB_CASSANDRA_CONN_STRING
AZURE_COSMOSDB_CASSANDRA_KEYSPACE
AZURE_COSMOSDB_CASSANDRA_PASS
AZURE_COSMOSDB_CASSANDRA_PORT
AZURE_COSMOSDB_CASSANDRA_URI
AZURE_COSMOSDB_CASSANDRA_USER

AZURE_COSMOSDB_EMULATOR_ACCT=localhost:8081
AZURE_COSMOSDB_EMULATOR_KEY=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==
AZURE_COSMOSDB_EMULATOR_URI=https://localhost:8081/

AZURE_COSMOSDB_GRAPHDB_ACCT
AZURE_COSMOSDB_GRAPHDB_COLNAME
AZURE_COSMOSDB_GRAPHDB_CONN_STRING
AZURE_COSMOSDB_GRAPHDB_DBNAME
AZURE_COSMOSDB_GRAPHDB_GRAPH
AZURE_COSMOSDB_GRAPHDB_KEY
AZURE_COSMOSDB_GRAPHDB_URI
AZURE_COSMOSDB_GRAPHDB_VIEWS
AZURE_COSMOSDB_GRAPHDB_YAML_CONFIG_FILE

AZURE_COSMOSDB_MONGODB_CONN_STRING
AZURE_COSMOSDB_MONGODB_DBNAME
AZURE_COSMOSDB_MONGODB_HOST
AZURE_COSMOSDB_MONGODB_PASS
AZURE_COSMOSDB_MONGODB_PORT
AZURE_COSMOSDB_MONGODB_USER

AZURE_COSMOSDB_SQLDB_ACCT
AZURE_COSMOSDB_SQLDB_COLLNAME
AZURE_COSMOSDB_SQLDB_CONN_STRING
AZURE_COSMOSDB_SQLDB_DBNAM
AZURE_COSMOSDB_SQLDB_KEY
AZURE_COSMOSDB_SQLDB_MULTI_REGION_WRITES
AZURE_COSMOSDB_SQLDB_PREF_REGION=East US
AZURE_COSMOSDB_SQLDB_PREF_REGIONS=East US
AZURE_COSMOSDB_SQLDB_RG
AZURE_COSMOSDB_SQLDB_URI
```


## About Chris

<p align="center"><img src="presentations/img/azure-spx-20190427a.jpg" width="95%"></p>

- Senior Cloud Solution Architect at Microsoft
- Specializing in Data & AI, and CosmosDB
- 30-years of AppDev experience
- chjoakim@microsoft.com
- @cjoakim
- https://www.linkedin.com/in/chris-joakim-4859b89/
- https://www.youracclaim.com/users/christopher-joakim/badges
- https://cjoakim.github.io
- Based in Charlotte, NC
