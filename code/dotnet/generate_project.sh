#!/bin/bash

# Use the dotnet CLI to bootstrap a dotnet project.
# Chris Joakim, Microsoft, 2021/06/24

project_name="sample_console_app"

echo ''
echo '=========='
echo 'removing output directory: '$project_name
rm -rf $project_name

echo ''
echo '=========='
echo 'dotnet --version  (5.0.202 is expected, as of June 2021)'
dotnet --version

echo ''
echo '=========='
echo 'generating project: '$project_name
dotnet new console -o $project_name

cd $project_name 

dotnet add package Microsoft.Azure.Cosmos
# dotnet add package Microsoft.EntityFrameworkCore.Cosmos
dotnet add package Azure.Storage.Blobs
dotnet add package Microsoft.Azure.DataLake.Store
dotnet add package CsvHelper
dotnet add package DocumentFormat.OpenXml 
dotnet add package Faker.Net

cat $project_name.csproj

dotnet list package
dotnet restore
dotnet build
dotnet run

echo ''
echo 'done'
