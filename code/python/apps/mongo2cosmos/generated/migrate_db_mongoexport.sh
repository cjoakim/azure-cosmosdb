#!/bin/bash

# Bash shell script to export each source collection via mongoexport.
#
# Database Name: migrate
# Generated on:  2021-03-02 14:46:49 


mongoexport \
  --host $MONGODB_HOST \
  --port $MONGODB_PORT \
  -d migrate \
  -u $MONGODB_USER \
  -p $MONGODB_PASS \
  -c title_basics \
  --ssl \
  --out data/mongo/migrate_title_basics_source.json

mongoexport \
  --host $MONGODB_HOST \
  --port $MONGODB_PORT \
  -d migrate \
  -u $MONGODB_USER \
  -p $MONGODB_PASS \
  -c name_basics \
  --ssl \
  --out data/mongo/migrate_name_basics_source.json


echo 'done'