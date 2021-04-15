#!/bin/bash

# Bash shell script to export each source collection via mongoexport.
#
# Database Name: dev
# Generated on:  2021-04-15 13:16:03 


mongoexport \
  --host $MONGODB_HOST \
  --port $MONGODB_PORT \
  -d dev \
  -u $MONGODB_USER \
  -p $MONGODB_PASS \
  -c imdb_names \
  --ssl \
  --out data/mongo/dev_imdb_names_source.json


echo 'done'