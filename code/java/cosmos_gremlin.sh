#!/bin/bash

# Execute the GremlinUtil Program via "mvn exec:java".
# Chris Joakim, Microsoft, 2020/11/19

mvn clean compile package

class="org.cjoakim.azure.cosmos.gremlin.GremlinUtil"


mvn exec:java -Dexec.mainClass=$class -Dexec.args="bom_query xxx bom_load bom_query"

echo 'done'
