# azure-cosmosdb

A collection of CosmosDB related [code](code/), [links](links.md), and 
[presentations](presentations/0_table_of_contents.md).

## CosmosDB

<p align="center"><img src="presentations/img/azure-cosmos-db-gray.png" width="95%"></p>

---

## Directory Structure of this Repo

```
    Directory                Status
    ---------                ------

├── automation               Azure ARM and az CLI deployment scripts
│   ├── arm                  
│   └── az                   
├── code                     CosmosDB SDK programming examples in each language
│   ├── dotnet               
│   ├── java                 
│   ├── java_spring          
│   ├── node                 
│   └── python               
│   └── rest                 HTTP REST API examples
├── data                     Common data files used across this repo      
├── dbs                      CosmosDB DBMS-Specific files
│   ├── cassandra
│   ├── graph
│   └── mongo                
├── docs
├── functions                
├── live_data_migrator       
├── notebooks                
├── presentations            start with file 0_table_of_contents.md          
├── server_side              Stored Prodedures, Triggers, UDF examples in js/ directory
└── synapse_pyspark          
```

This repo is a **work in progress; not all of the above are  at this time**.

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

- **NoSQL Technical Specialist Global Black Belt at Microsoft**
- Specializing in Data & AI, and **CosmosDB**
- 30+ years of AppDev experience
- 5-years of Azure Architect experience at Microsoft
- chjoakim@microsoft.com
- https://www.linkedin.com/in/chris-joakim-4859b89/
- https://www.youracclaim.com/users/christopher-joakim/badges
- https://twitter.com/cjoakim?lang=en
- https://cjoakim.github.io
- Based in Charlotte, NC, USA
