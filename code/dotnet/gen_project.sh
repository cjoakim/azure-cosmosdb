#!/bin/bash

# Use the dotnet CLI to generate/bootstrap a project.
# Chris Joakim, Microsoft, 2021/04/27

project_name="multi_region"

echo ''
echo '=========='
echo 'removing any output files...'
rm -rf $project_name

echo ''
echo '=========='
echo 'dotnet --version  (5.0.x is expected, as of April 2021)'
dotnet --version

echo ''
echo '=========='
echo 'creating project: '$project_name
dotnet new console -o $project_name
cd $project_name 
dotnet add package Microsoft.Azure.Cosmos
dotnet add package CsvHelper
cat loader.csproj
dotnet list package
dotnet restore
dotnet build
dotnet run

echo ''
echo 'done'
