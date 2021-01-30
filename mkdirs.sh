#!/bin/bash

# Bash script to boostrap the structure of this repo.
# Chris Joakim, 2021/01/30

mkdir -p automation/arm
mkdir -p automation/az
touch automation/readme.md
touch automation/arm/readme.md
touch automation/az/readme.md

mkdir -p data/airports
mkdir -p data/amtrak
mkdir -p data/postal
mkdir -p data/graph/npm
mkdir -p data/graph/amtrak
touch data/readme.md
touch data/airports/readme.md
touch data/amtrak/readme.md
touch data/postal/readme.md
touch data/graph/npm/readme.md
touch data/graph/amtrak/readme.md

mkdir -p dotnet
mkdir -p java
mkdir -p java_spring
mkdir -p node
mkdir -p python
touch dotnet/readme.md
touch java/readme.md
touch java_spring/readme.md
touch node/readme.md
touch python/readme.md

mkdir -p graph/v1
mkdir -p graph/v2
touch graph/readme.md
touch graph/v1/readme.md
touch graph/v2/readme.md

mkdir -p cassandra/ddl
mkdir -p mongo/ddl
touch cassandra/readme.md
touch mongo/readme.md

mkdir -p functions
touch functions/readme.md

mkdir -p live_data_migrator
touch live_data_migrator/readme.md

mkdir -p notebooks
touch notebooks/readme.md

mkdir -p server_side
touch server_side/readme.md

mkdir -p synapse_pyspark
touch synapse_pyspark/readme.md

mkdir -p presentations
mkdir -p presentations/img
touch presentations/readme.md
