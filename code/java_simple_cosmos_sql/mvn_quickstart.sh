#!/bin/bash

# Bash script to use a Maven (mvn) Archetype to bootstrap a new Java project.
# Chris Joakim, Microsoft, 2021/02/18
# 
# Links:
# https://maven.apache.org/guides/introduction/introduction-to-archetypes.html
# https://maven.apache.org/archetypes/maven-archetype-quickstart/

# mvn archetype:generate --help

mvn archetype:generate \
    -DgroupId="org.cjoakim.azure.cosmos.sql" \
    -DartifactId="sample" \
    -Dversion="1.0" \
    -DarchetypeGroupId="org.apache.maven.archetypes" \
    -DarchetypeArtifactId="maven-archetype-quickstart" \
    -DarchetypeVersion="1.4" \
    --batch-mode

echo 'done'
