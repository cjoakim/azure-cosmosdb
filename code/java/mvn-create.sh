#!/bin/bash

# This shell script was used to bootstrap this Maven project
# Chris Joakim, Microsoft, 2021/05/24

# https://maven.apache.org/guides/introduction/introduction-to-archetypes.html

mvn archetype:generate \
    -DgroupId=org.cjoakim.cosmos \
    -DartifactId=async \
    -DarchetypeArtifactId=maven-archetype-quickstart \
    -DinteractiveMode=false

# mvn archetype:generate --batch-mode \
#     -DarchetypeGroupId=com.microsoft.azure \
#     -DarchetypeArtifactId=azure-functions-archetype \
#     -DappName=$FUNCTION_APP \
#     -DresourceGroup=$RESOURCE_GROUP \
#     -DappRegion=$LOCATION \
#     -DgroupId=com.example \
#     -DartifactId=telemetry-functions

echo 'done'
