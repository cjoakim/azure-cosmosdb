#!/bin/bash

# Deploy the Azure Function App containing the CosmosPlantsUpdate Function.
# Chris Joakim, Microsoft, 2021/03/05

app_name="cjoakimpyfunctions"

echo 'publishing function app named: '$app_name

func azure functionapp publish $app_name

echo 'done'
