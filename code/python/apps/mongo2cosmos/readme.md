# MongoDB-to-CosmosDB/Mongo Migration

## Process

- Extract the **metadata** about the source MongoDB database
  - See mongo_metadata.py

- **Generate** shell scripts and other code from the above metadata
  - Generate mongoexport script(s) from source database
  - Generate shell script to transform the source mongoexport files to target files

- **Execute the mongoexport file Transformations**
  - Simple and fast Python code can be used for this
    - Read the source mongoexport file
    - Add the pk and doctype attributes
    - Produce a mongoexport file in the format for the target database
    - Repeat as necessary for each collection and mongoexport file
    - Yes, use code generation

- **Import the transformed mongoexport files into CosmosDB**
  - One approach is to use the **mongoimport** utility
  - Another approach is to use **Azure Data Factory**
