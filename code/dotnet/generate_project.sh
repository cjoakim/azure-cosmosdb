#!/bin/bash

# Use the dotnet CLI to bootstrap a dotnet project.
# Chris Joakim, Microsoft, September 2021

project_name="cosmos_sql_bulk_loader"

echo ''
echo '=========='
echo 'removing output directory: '$project_name
rm -rf $project_name

echo ''
echo '=========='
echo 'dotnet --version'  # 5.0.202 is expected
dotnet --version

echo ''
echo '=========='
echo 'generating project: '$project_name
dotnet new console -o $project_name

cd $project_name 

dotnet add package Microsoft.Azure.Cosmos
dotnet add package Faker.Net

# dotnet add package Microsoft.Azure.Cosmos
# dotnet add package Microsoft.EntityFrameworkCore.Cosmos
# dotnet add package Azure.Storage.Blobs
# dotnet add package Microsoft.Azure.DataLake.Store
# dotnet add package CsvHelper
# dotnet add package DocumentFormat.OpenXml 
# dotnet add package Faker.Net
# dotnet add package MongoDB.Driver
# https://www.nuget.org/packages/MongoDB.Driver/
# https://docs.mongodb.com/drivers/csharp/

cat $project_name.csproj

dotnet list package
dotnet restore
dotnet build
dotnet run

echo ''
echo 'done'



