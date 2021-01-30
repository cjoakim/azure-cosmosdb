#!/bin/bash

# Deploy the Azure Function App containing the CosmosPlantsUpdate Function.
# Chris Joakim, Microsoft, 2020/10/10

app_name="cjoakimsynapse2f"

echo 'publishing function app named: '$app_name

func azure functionapp publish $app_name

echo 'done'
