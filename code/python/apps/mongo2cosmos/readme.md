# MongoDB-to-CosmosDB/Mongo Migration

## Process

- Extract the **metadata** about the source MongoDB database
  - See **mongo_metadata.py**

- **Generate** shell scripts and other code from the above metadata
  - Generate mongoexport script(s) from source database
  - Generate shell script to transform the source mongoexport files to target files

- **Execute the mongoexport file Transformations**
  - Simple and fast Python code can be used for this
    - Read the source mongoexport file
    - Add the pk and doctype attributes
    - Do other transformations as necessary
    - Produce a mongoexport file in the format for the target database
    - Repeat as necessary for each collection and mongoexport file
    - Yes, use code generation
  - See **transform_mongoexports.py** and **transform_mongoexports.sh**

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

<p align="center"><img src="img/adf-job-created.png"></p>

---

<p align="center"><img src="img/adf-job-deployed.png"></p>

---

<p align="center"><img src="img/adf-copy-running.png"></p>

---

<p align="center"><img src="img/adf-job-in-progress-details.png"></p>

---

<p align="center"><img src="img/adf-docs-in-cosmosdb.png"></p>
