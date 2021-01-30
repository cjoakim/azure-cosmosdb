#!/bin/bash

# Execute the main Program via "mvn exec:java".
# Chris Joakim, Microsoft, 2020/11/15

mvn clean compile package

airportsFile="/Users/cjoakim/github/cj-azure/lang/dotnet/cosmos_sql/data/airports/openflights_airports.csv"


#class="com.microsoft.csu.cdbhack.Program"
#class="org.cjoakim.azure.AppConfig"
#class="org.cjoakim.azure.App"
#class="org.cjoakim.azure.storage.BlobUtil"
#class="org.cjoakim.azure.cosmosdb.CosmosDbUtil"
class="org.cjoakim.azure.cosmosdb.GremlinUtil"

#mvn exec:java -Dexec.mainClass=org.cjoakim.azure.App -Dexec.args="woodchucks"

mvn exec:java -Dexec.mainClass=$class -Dexec.args="xxx yyy zzz"

echo 'done'
