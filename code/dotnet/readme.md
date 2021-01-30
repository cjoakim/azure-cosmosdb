# Azure w/DotNet

## Links

- https://github.com/AzureCosmosDB/labs
- https://github.com/AzureCosmosDB/labs/blob/master/dotnet/labs/08-change_feed_with_azure_functions.md

## DotNet Core Project Setup

```
$ dotnet --version
5.0.100-rc.2.20479.15

$ dotnet new console -o cart_data_generator
$ cd cart_data_generator/
$ dotnet add package Microsoft.Azure.Cosmos
$ dotnet add package Bogus
$ dotnet list package
Project 'cart_data_generator' has the following package references
   [net5.0]:
   Top-level Package             Requested   Resolved
   > Bogus                       31.0.3      31.0.3
   > Microsoft.Azure.Cosmos      3.14.0      3.14.0
```

add package Microsoft.Azure.DataLake.Store
