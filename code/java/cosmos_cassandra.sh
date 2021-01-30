#!/bin/bash

# Execute the GremlinUtil Program via "mvn exec:java".
# Chris Joakim, Microsoft, 2020/11/20

mvn clean compile package

class="org.cjoakim.azure.cosmos.cassandra.CassandraUtil"

mvn exec:java -Dexec.mainClass=$class -Dexec.args="connect a b c"

echo 'done'
