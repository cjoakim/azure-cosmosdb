#!/bin/bash

# Executes this Spring Boot app.
# Chris Joakim, 2021/04/04

./build.sh

jar="target/travel-0.0.1.jar"
functions="loadDB"

db_url="jdbc:postgresql://"$AZURE_PG_SERVER_FULL_NAME":"$AZURE_PG_PORT"/"$AZURE_PG_DATABASE

java -Xmx200m \
    -Ddebug=true \
    -Dspring.profiles.active=default \
    -Dspring.datasource.url=$db_url \
    -Dspring.datasource.username=$AZURE_PG_USER \
    -Dspring.datasource.password=$AZURE_PG_PASS \
    -jar $jar $functions
