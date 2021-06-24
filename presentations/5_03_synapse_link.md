# 5.03 - Synapse Link

## Features

- **Free ETL**
- **Low Cost Analytical Storage**
- **"Parquet-like" format - Readable as a PySpark Dataframe**
- **Readable with T-SQL** (SQL DW)
- **TTL - both CosmosDB and Analytical Storage**

## Synapse and Synapse Link

<p align="center"><img src="img/synapse-analytics-cosmos-db-architecture.png" width="80%"></p>

---

## PySpark Notebook in Synapse

<p align="center"><img src="img/pyspark-notebook-example.png" width="80%"></p>

```
# Read from Cosmos DB analytical store into a Spark DataFrame and display 10 rows from the DataFrame

df = spark.read\
    .format("cosmos.olap")\
    .option("spark.synapse.linkedService", "cosmos_dev_db")\
    .option("spark.cosmos.container", "plants")\
    .load()

display(df.limit(10))
```

---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](5_02_azure_functions.md) &nbsp; | &nbsp; [next](5_04_azure_search.md) &nbsp;
