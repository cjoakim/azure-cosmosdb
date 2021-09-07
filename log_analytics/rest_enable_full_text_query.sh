#!/bin/bash

# Enable query text in CosmosDB Log Analytics.
# Chris Joakim, Microsoft, 2021/09/07


subs=$AZURE_SUBSCRIPTION_ID
rg="cjoakimcsl" 
acct="cjoakimcslcosmos"
uri='https://management.azure.com/subscriptions/'$subs'/resourceGroups/'$rg'/providers/Microsoft.DocumentDB/databaseAccounts/'$acct'/?api-version=2021-05-01-preview'
query='{AcctName:name,diagnosticLogSettings:properties.diagnosticLogSettings}' 

echo 'subs:  '$subs 
echo 'rg:    '$rg 
echo 'acct:  '$acct 
echo 'uri:   '$uri 
echo 'query: '$query 

echo 'initial query...'
az rest --method GET --uri $uri --query $query

echo 'patching...'
az rest --method PATCH --uri $uri --body '{"properties": {"diagnosticLogSettings": {"enableFullTextQuery": "True"}}}'

echo 'sleeping...'
sleep 20

echo 'query after patch...'
az rest --method GET --uri $uri --query $query

echo 'done'
