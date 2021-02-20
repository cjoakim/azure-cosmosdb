# MongoDB-to-CosmosDB/Mongo Migration

## Process

- Extract the **metadata** about the source MongoDB database
  - See **mongo_metadata.py**

- **Generate** shell scripts and other code from the above metadata
  - Generate mongoexport script(s) from source database
  - Generate shell script to transform the source mongoexport files to target files
  - Code generation not yet implemented in this repo; pending customer details
  - Python and [Jinja templates](https://palletsprojects.com/p/jinja/) are perfect for this

- **Execute the mongoexport file Transformations**
  - Simple and fast Python code can be used for this
    - Read the source mongoexport file
    - Add the pk and doctype attributes
    - Do other transformations as necessary
    - Produce a mongoexport file in the format for the target database
    - Repeat as necessary for each collection and mongoexport file
    - Yes, use code generation
  - See **transform_mongoexports.py** and **transform_mongoexports.sh**
    - Transform a 1-million row file in under 12-seconds

  - Note: this repo uses **IMDb** as large dataset for testing purposes
    - This is a large public domain dataset
    - Download the data with script data/imdb/curl_get_imdb_datasets.sh
    - See **wrangle_imdb.sh** and **wrangle_imdb.py** which reads the IMDb TSV files and transforms them into a working mongoexport format
    - Using this IMDb data simulates a large customer database

- **Create the CosmosDB Target Database, Collections, Indexes**
  - Create the CosmosDB account, database, and set the shared throughput (Azure Portal)
  - Execute generated scripts to create the collections and indexes
  - See examples: **mongo_init.sh** and **mongo/azure_init.ddl**

- **Import the transformed mongoexport files into CosmosDB**
  - One approach is to use the **mongoimport** utility
    - See **mongo_load.sh**
  - Another approach is to use **Azure Data Factory**
    - See screen shots below
    - Source is the transformed mongoexport file(s) in **Azure Blob Storage**
      - [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/)
    - Target is the CosmosDB/Mongo database collection
  - Another approach is to use a programming language SDK to load CosmosDB from the transformed mongoexport files (DotNet, Java, Python/pymongo, Node, etc)


---

### Azure Data Factory (ADF)

The following are screen-shots of creating and executing an ADF Copy job.

#### Create the ADF Copy Job

<p align="center"><img src="img/adf-job-created.png"></p>

---

#### ADF Copy Job is Deployed

<p align="center"><img src="img/adf-job-deployed.png"></p>

---

#### ADF Copy Job Running

<p align="center"><img src="img/adf-copy-running.png"></p>

---

#### ADF Copy Job Running - click into Details

<p align="center"><img src="img/adf-job-in-progress-details.png"></p>

---

#### View Documents in CosmosDB as the Job is Running

<p align="center"><img src="img/adf-docs-in-cosmosdb.png"></p>

---

#### ADF Copy Job Completed Successfully

Note the exact record count, 1,699,998.  ADF is solid.

<p align="center"><img src="img/adf-job-completed.png"></p>

---

#### Connect to CosmosDB with the mongo shell program to verify


```
$ ./mongo_shell.sh azure
```

```
MongoDB server version: 3.6.0

globaldb:PRIMARY> show dbs
dev      0.000GB
migrate  0.000GB

globaldb:PRIMARY> use migrate
switched to db migrate

globaldb:PRIMARY> show collections
combined
name_basics
title_basics

globaldb:PRIMARY> db.combined.count()
1699998

globaldb:PRIMARY> db.combined.findOne()
{
	"_id" : "603111acbeea9dc5cb886b0d",
	"seq" : 2205,
	"nconst" : "nm0002207",
	"primaryName" : "Richard Franklin",
	"birthYear" : "1948",
	"deathYear" : "2007",
	"primaryProfession" : [
		"director",
		"producer",
		"writer"
	],
	"knownForTitles" : [
		"tt0080453",
		"tt0078067",
		"tt0091415",
		"tt0113337"
	],
	"pk" : "nm0002207",
	"doctype" : "name_basics"
}
globaldb:PRIMARY>
```
