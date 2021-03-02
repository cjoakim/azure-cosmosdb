#!/bin/bash

# Bash shell script to execute mongoexport file transformations
# from "source" to "target" database format.
#
# Database Name: migrate
# Generated on:  2021-03-02 14:46:49 

# Execute the transformations for the database:

python transform_mongoexports.py transform \
  title_basics \
  data/mongo/title_basics_source.json \
  data/mongo/title_basics_target.json

python transform_mongoexports.py transform \
  name_basics \
  data/mongo/name_basics_source.json \
  data/mongo/name_basics_target.json


# Verify the transformations for the database:

python transform_mongoexports.py verify_transformation \
  title_basics 700 \
  data/mongo/title_basics_source.json \
  data/mongo/title_basics_target.json

python transform_mongoexports.py verify_transformation \
  name_basics 1000 \
  data/mongo/name_basics_source.json \
  data/mongo/name_basics_target.json


echo 'done'