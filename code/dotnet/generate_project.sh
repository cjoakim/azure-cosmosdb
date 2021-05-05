#!/bin/bash

# Use the dotnet CLI to bootstrap dotnet project(s).
# Samples:
# - https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-dotnet
#
# Chris Joakim, Microsoft, 2021/05/05

project_name="storage_client"

echo ''
echo '=========='
echo 'removing output directory: '$project_name
rm -rf $project_name

echo ''
echo '=========='
echo 'dotnet --version  (5.0.x is expected, as of May 2021)'
dotnet --version

echo ''
echo '=========='
echo 'generating project: '$project_name
dotnet new console -o $project_name
cd $project_name 
dotnet add package Microsoft.Azure.Cosmos
dotnet add package Azure.Storage.Blobs
dotnet add package CsvHelper
dotnet add package Faker.Net
cat $project_name.csproj
dotnet list package
dotnet restore
dotnet build
dotnet run

echo ''
echo 'done'
