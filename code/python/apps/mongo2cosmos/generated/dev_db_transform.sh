#!/bin/bash

# Bash shell script to execute mongoexport file transformations
# from "source" to "target" database format.
#
# Database Name: dev
# Generated on:  2021-04-15 13:16:03 

# Execute the transformations for the database:

python transform_mongoexports.py transform \
  imdb_names \
  data/mongo/imdb_names_source.json \
  data/mongo/imdb_names_target.json


# Verify the transformations for the database:

python transform_mongoexports.py verify_transformation \
  imdb_names 5000 \
  data/mongo/imdb_names_source.json \
  data/mongo/imdb_names_target.json


echo 'done'