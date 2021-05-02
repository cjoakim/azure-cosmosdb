#!/bin/bash

# Use the dotnet CLI to bootstrap dotnet project(s).
# Chris Joakim, Microsoft, 2021/05/02

project_name="json_loader"

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
dotnet add package CsvHelper
dotnet add package Faker.Net
cat $project_name.csproj
dotnet list package
dotnet restore
dotnet build
dotnet run

echo ''
echo 'done'
