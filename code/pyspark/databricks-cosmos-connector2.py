# Databricks notebook source
# See https://docs.databricks.com/_static/notebooks/data-import/azure-blob-store.html
# https://docs.microsoft.com/en-us/azure/databricks/data/data-sources/azure/azure-storage

# Configure the Storage Input
storage_account_name = "cjoakimm2cstorage"
blob_container = "pyspark"

spark.conf.set(
  "fs.azure.account.key.cjoakimm2cstorage.blob.core.windows.net",
  "...secret...")
spark.conf.set(
  "fs.azure.sas.pyspark.cjoakimm2cstorage.blob.core.windows.net",
  "https://cjoakimm2cstorage.blob.core.windows.net/pyspark?sv=2020-04-08&st=2021-06-18T19%3A23%3A30Z&se=2021-12-31T20%3A23%3A00Z&...secret...")

# URL: https://cjoakimm2cstorage.blob.core.windows.net/travel-routes-adf/openflights__routes__wrangled.json

# Configure the CosmosDB Output
cosmosEndpoint = "https://cjoakimcosmossql.documents.azure.com:443/"
cosmosMasterKey = "...secret..."
cosmosDatabaseName = "dev"
cosmosContainerName = "airports2"

writeCfg = {
  "spark.cosmos.accountEndpoint": cosmosEndpoint,
  "spark.cosmos.accountKey": cosmosMasterKey,
  "spark.cosmos.database": cosmosDatabaseName,
  "spark.cosmos.container": cosmosContainerName,
  "spark.cosmos.write.strategy": "ItemOverwrite",
}

spark.conf.set("spark.sql.catalog.cosmosCatalog", "com.azure.cosmos.spark.CosmosCatalog")
spark.conf.set("spark.sql.catalog.cosmosCatalog.spark.cosmos.accountEndpoint", cosmosEndpoint)
spark.conf.set("spark.sql.catalog.cosmosCatalog.spark.cosmos.accountKey", cosmosMasterKey)

# spark.sql("CREATE DATABASE IF NOT EXISTS cosmosCatalog.{};".format(cosmosDatabaseName))
# spark.sql("CREATE TABLE IF NOT EXISTS cosmosCatalog.{}.{} using cosmos.oltp TBLPROPERTIES(partitionKeyPath = '/city', manualThroughput = '1100')".format(cosmosDatabaseName, cosmosContainerName))

spark.sql("CREATE TABLE IF NOT EXISTS cosmosCatalog.{}.{} using cosmos.oltp TBLPROPERTIES(partitionKeyPath = '/pk')".format(cosmosDatabaseName, cosmosContainerName))


# COMMAND ----------

# Read the Storage Blob as df 

df = spark.read.json("wasbs://pyspark@cjoakimm2cstorage.blob.core.windows.net/")

# # Display the observed schema, or structure of the DataFrame.
display(df.printSchema())


# COMMAND ----------

# Print the number of rows and columns in the DataFrame
print((df.count(), len(df.columns)))   # (67663, 12)


# COMMAND ----------

print(df.columns)


# COMMAND ----------

# Print up to 10 rows of the DataFrame
display(df.limit(20))


# COMMAND ----------


# # Wrangle/prune the data
# df2 = df.drop("_id")
# df3 = df2.drop("x")
# df4 = df3.drop("t")
# df5 = df4.drop("doctype")
# df6 = df5.drop("openflights_from_airport")
# df7 = df6.drop("openflights_to_airport")
# df8 = df7.drop("openflights_airline_id")

# Print the final set of columns
print(df.columns)



# COMMAND ----------


display(df.limit(100))

# COMMAND ----------

 
df.toDF("altitude","city","country","iata_code","id","latitude","location","longitude","name","pk","timezone_code","timezone_num")\
  .write.format("cosmos.oltp").options(**writeCfg).mode("APPEND").save()

