# azure-cosmosdb links

A collection of CosmosDB-related links that I find useful.

## CosmosDB General

- [Documentation Home](https://docs.microsoft.com/en-us/azure/cosmos-db/)
- [Partitioning and Horizontal Scaling](https://docs.microsoft.com/en-us/azure/cosmos-db/partitioning-overview)
- [Request Units](https://docs.microsoft.com/en-us/azure/cosmos-db/request-units)
- [Autoscale](https://docs.microsoft.com/en-us/azure/cosmos-db/provision-throughput-autoscale)
- [Consistency Levels](https://docs.microsoft.com/en-us/azure/cosmos-db/consistency-levels)
- [Jupyter Notebooks - Python and C#](https://docs.microsoft.com/en-us/azure/cosmos-db/cosmosdb-jupyter-notebooks)
- [az CLI](https://docs.microsoft.com/en-us/cli/azure/cosmosdb?view=azure-cli-latest)
- [Emulator](https://docs.microsoft.com/en-us/azure/cosmos-db/local-emulator)
- [Serverless](https://docs.microsoft.com/en-us/azure/cosmos-db/serverless)
- [Blog](https://devblogs.microsoft.com/cosmosdb/)

---

## APIs and Features

### CosmosDB SQL 

- [Modeling](https://docs.microsoft.com/en-us/azure/cosmos-db/modeling-data)
- [SQL Syntax](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-query-getting-started)
- [Indexing](https://docs.microsoft.com/en-us/azure/cosmos-db/index-overview)
- [Stored procedures, triggers, UDFs](https://docs.microsoft.com/en-us/azure/cosmos-db/stored-procedures-triggers-udfs)
- [Geospatial and GeoJSON](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-query-geospatial-intro)
- [Bulk Executor Library](https://docs.microsoft.com/en-us/azure/cosmos-db/bulk-executor-overview)

### CosmosDB Mongo 

- [https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb-introduction](https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb-introduction)
- [MongoDB Indexing](https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb-indexing)
- [MongoDB 3.6 Support](https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb-feature-support-36)
- [Change streams](https://docs.microsoft.com/en-us/azure/cosmos-db/mongodb-change-streams?tabs=javascript)

#### Open-Source Mongo Libraries

- [pymongo @ PyPI](https://pypi.org/project/pymongo/)
- [pymongo docs](https://pymongo.readthedocs.io/en/stable/)
- [mongoose @ npm](https://www.npmjs.com/package/mongoose)

### CosmosDB Graph/Gremlin

- [Intro to Gremlin API in Azure Cosmos DB](https://docs.microsoft.com/en-us/azure/cosmos-db/graph-introduction)
- [Apache TinkerPop Project](http://tinkerpop.apache.org/)
- [Practical Gremlin: An Apache TinkerPop Tutorial](http://kelvinlawrence.net/book/Gremlin-Graph-Guide.html)

### CosmosDB Cassandra

- [Intro to the Azure Cosmos DB Cassandra API](https://docs.microsoft.com/en-us/azure/cosmos-db/cassandra-introduction)

### Change Feed

- [Change Feed in Azure Cosmos DB](https://docs.microsoft.com/en-us/azure/cosmos-db/change-feed)
- [Change Feed with Azure Functions](https://docs.microsoft.com/en-us/azure/cosmos-db/change-feed-functions)
- [Change Feed with Azure Cosmos DB .NET SDK Version 3](https://docs.microsoft.com/en-us/azure/cosmos-db/change-feed-processor)

### Synapse Link

- [What is Azure Synapse Link?](https://docs.microsoft.com/en-us/azure/cosmos-db/synapse-link)
- [Architecture Diagram](https://docs.microsoft.com/en-us/azure/cosmos-db/media/synapse-link/synapse-analytics-cosmos-db-architecture.png)

### REST

- [Azure CosmosDB/SQL REST API Reference](https://docs.microsoft.com/en-us/rest/api/cosmos-db/)

### Other

- [Azure CosmosDB Data Migration Tool](https://docs.microsoft.com/en-us/azure/cosmos-db/import-data)
- [Live Data Migrator](https://github.com/Azure-Samples/azure-cosmosdb-live-data-migrator)
- [Azure Updates](https://azure.microsoft.com/en-us/updates/)
- [Databricks CosmosDB Connector](https://docs.databricks.com/data/data-sources/azure/cosmosdb-connector.html)

---

## SDKs

### Dotnet

- [NET SDK v3 for SQL API](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-dotnet-standard)
- [Microsoft.Azure.Cosmos @ NuGet](https://www.nuget.org/packages/Microsoft.Azure.Cosmos/)
- [azure-cosmos-dotnet-v3 GitHub](https://github.com/Azure/azure-cosmos-dotnet-v3)
- [Azure.Cosmos package docs](https://docs.microsoft.com/en-us/dotnet/api/overview/azure/cosmosdb/client?view=azure-dotnet)
- [Sample .NET console app](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-get-started)
- [EF Core Azure Cosmos DB Provider](https://docs.microsoft.com/en-us/ef/core/providers/cosmos/?tabs=dotnet-core-cli#get-started)

### Java 

- [Java SDK for SQL API](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-java)
- [azure-documentdb @ maven.org](https://search.maven.org/search?q=g:com.microsoft.azure%20AND%20a:azure-documentdb)
- [com.microsoft.azure.documentdb package docs](https://docs.microsoft.com/en-us/java/api/com.microsoft.azure.documentdb?view=azure-java-stable)
- [V4 SDK Sample App](https://docs.microsoft.com/en-us/azure/cosmos-db/create-sql-api-java?tabs=sync)
- [Java on Azure Learning Path](https://docs.microsoft.com/en-us/learn/paths/java-on-azure/?WT.mc_id=java-11777-judubois)

### Java/Spring

- [Spring Data and CosmosDB](https://docs.microsoft.com/en-us/azure/developer/java/spring-framework/how-to-guides-spring-data-cosmosdb)
- [Spring Boot Starter](https://docs.microsoft.com/en-us/azure/developer/java/spring-framework/configure-spring-boot-starter-java-app-with-cosmos-db)

### Node

- [Node.js SDK for SQL API](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-node)
- [@azure/cosmos @ npm](https://www.npmjs.com/package/@azure/cosmos)
- [@azure/cosmos package docs](https://docs.microsoft.com/en-us/javascript/api/%40azure/cosmos/?preserve-view=true&view=azure-node-latest)
- [Code Samples](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-nodejs-samples)

### Python

- [Python SDK for SQL API](https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-sdk-python)
- [azure-cosmos @ PyPI](https://pypi.org/project/azure-cosmos/)
- [cosmos package docs](https://docs.microsoft.com/en-us/python/api/azure-cosmos/azure.cosmos?view=azure-python)

--- 

## Curated cjoakim Repos

- https://github.com/cjoakim/azure-adventureworks-to-cosmos
- https://github.com/cjoakim/azure-cosmosdb-cost-calculator
- https://github.com/cjoakim/azure-cosmos-change-feed-gremlin
- https://github.com/cjoakim/azure-iot-cosmosdb-synapse
- https://github.com/cjoakim/azure-cosmosdb-nosql-hackathon
- https://github.com/Azure-Samples/azure-cosmos-db-graph-npm-bom-sample
- https://github.com/cjoakim/m26-py
