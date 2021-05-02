#!/bin/bash

# Use the dotnet CLI to bootstrap a dotnet solution and project(s).
# Chris Joakim, Microsoft, 2021/05/02

solution_name="json_loader"

echo ''
echo '=========='
echo 'removing any output files...'
rm -rf $solution_name

echo ''
echo '=========='
echo 'dotnet --version  (5.0.x is expected, as of May 2021)'
dotnet --version

echo ''
echo '=========='
echo 'creating the solution...'
dotnet new sln -o $solution_name
cd $solution_name

echo ''
echo '=========='
echo 'creating the loader project...'
dotnet new console -o loader
cd loader 
dotnet add package Microsoft.Azure.Cosmos
dotnet add package CsvHelper
cat loader.csproj
dotnet list package
dotnet restore
dotnet build
dotnet run

echo ''
echo '=========='
echo 'creating the loader.tests project...'
cd ..
dotnet new xunit -o loader.tests
cd loader.tests
dotnet add package Faker.Net
dotnet add package ReportGenerator
dotnet add package coverlet.collector
dotnet add reference ../loader/loader.csproj
cat loader.tests.csproj
dotnet list package
dotnet restore
dotnet build
dotnet run

cd ..

echo ''
echo '=========='
echo 'adding projects to solution...'
pwd

dotnet sln $solution_name.sln add loader/loader.csproj
dotnet sln $solution_name.sln add loader.tests/loader.tests.csproj
dotnet build

echo ''
echo 'done'
