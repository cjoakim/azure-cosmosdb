# Azure Automation


## Summary

- Azure Resource Manager, ARM - for a group of resources 
  - deploy the ARM template with PowerShell or az CLI

- PowerShell cmdlets - deploy individual resources

- az CLI commands - deploy individual resources

- Bicep - new syntax that transpiles to ARM Templates

- Azure DevOps - execute any of the above in a DevOps Pipeline

---

## Azure Resource Manager, ARM

- [What are ARM templates?](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/overview)
- Declarative templates rather than scripts
- Desired State Configuration 
- Templates are **idempotent**; implement **diff** functionality
- JSON syntax
- Deploy, manage, and monitor all the resources for your **solution as a group**, not individually
- Can be exported from Azure Portal from existing resources

### Deploy an ARM Template with PowerShell

https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/template-tutorial-create-first-template?tabs=azure-powershell#deploy-template

Use cmdlet **New-AzResourceGroupDeployment**

```
$templateFile = "{provide-the-path-to-the-template-file}"
New-AzResourceGroupDeployment `
  -Name blanktemplate `
  -ResourceGroupName myResourceGroup `
  -TemplateFile $templateFile
```

### Deploy an ARM Template with the az CLI

The **az** program is portable across Windows, Linux, and macOS and offers the exact
same syntax on these three platforms.

Example az command:
```
az group deployment create \
  --name $dep_name \
  --resource-group $resource_group \
  --template-file storage-template.json \
  --parameters @storage-parameters.json
```

---

## PowerShell

- Alternatively, provision **individual** Azure Resources with PowerShell cmdlets
- [Manage Azure Cosmos DB Core](https://docs.microsoft.com/en-us/azure/cosmos-db/manage-with-powershell)

Use the **New-AzCosmosDBAccount** cmdlet, for example.

```
$resourceGroupName = "myResourceGroup"
$accountName = "mycosmosaccount"
$apiKind = "Sql"
$consistencyLevel = "BoundedStaleness"
$maxStalenessInterval = 300
$maxStalenessPrefix = 100000
$locations = @()
$locations += New-AzCosmosDBLocationObject -LocationName "East US" -FailoverPriority 0 -IsZoneRedundant 0
$locations += New-AzCosmosDBLocationObject -LocationName "West US" -FailoverPriority 1 -IsZoneRedundant 0

New-AzCosmosDBAccount `
    -ResourceGroupName $resourceGroupName `
    -LocationObject $locations `
    -Name $accountName `
    -ApiKind $apiKind `
    -EnableAutomaticFailover:$true `
    -DefaultConsistencyLevel $consistencyLevel `
    -MaxStalenessIntervalInSeconds $maxStalenessInterval `
    -MaxStalenessPrefix $maxStalenessPrefix
```

Get the throughput of a container with **Get-AzCosmosDBSqlContainerThroughput**.

```
$resourceGroupName = "myResourceGroup"
$accountName = "mycosmosaccount"
$databaseName = "myDatabase"
$containerName = "myContainer"

Get-AzCosmosDBSqlContainerThroughput `
    -ResourceGroupName $resourceGroupName `
    -AccountName $accountName `
    -DatabaseName $databaseName `
    -Name $containerName
```

## az Command Line Tool

- Alternatively, provision **individual** Azure Resources with PowerShell cmdlets
- [List of Commands](https://docs.microsoft.com/en-us/cli/azure/cosmosdb?view=azure-cli-latest)

```
$ az cosmosdb --help

Group
    az cosmosdb : Manage Azure Cosmos DB database accounts.

Subgroups:
    cassandra                   : Manage Cassandra resources of Azure Cosmos DB account.
    gremlin                     : Manage Gremlin resources of Azure Cosmos DB account.
    keys                        : Manage Azure Cosmos DB keys.
    mongodb                     : Manage MongoDB resources of Azure Cosmos DB account.
    network-rule                : Manage Azure Cosmos DB network rules.
    private-endpoint-connection : Manage Azure Cosmos DB private endpoint connections.
    private-link-resource       : Manage Azure Cosmos DB private link resources.
    sql                         : Manage SQL resources of Azure Cosmos DB account.
    table                       : Manage Table resources of Azure Cosmos DB account.

Commands:
    check-name-exists           : Checks if an Azure Cosmos DB account name exists.
    create                      : Creates a new Azure Cosmos DB database account.
    delete                      : Deletes an Azure Cosmos DB database account.
    failover-priority-change    : Changes the failover priority for the Azure Cosmos DB database
                                  account.
    list                        : List Azure Cosmos DB database accounts.
    show                        : Get the details of an Azure Cosmos DB database account.
    update                      : Update an Azure Cosmos DB database account.

For more specific examples, use: az find "az cosmosdb"
```

Example: How I redeploy my CosmosDB/SQL account; **az cosmosdb create**

```
    echo 'creating cosmos acct: '$cosmos_sql_acct_name
    az cosmosdb create \
        --name $cosmos_sql_acct_name \
        --resource-group $cosmos_sql_rg \
        --subscription $subscription \
        --locations regionName=$cosmos_sql_region failoverPriority=0 isZoneRedundant=False \
        --default-consistency-level $cosmos_sql_acct_consistency \
        --enable-multiple-write-locations true \
        --enable-analytical-storage true \
        --kind $cosmos_sql_acct_kind \
        > data/output/cosmos_sql_acct_create.json
```

## Bicep

- [Bicep Tutorial](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/bicep-tutorial-create-first-bicep?tabs=azure-powershell)

---

## Azure DevOps

- [Azure DevOps](https://azure.microsoft.com/en-us/services/devops/)
- Visual Interface or YAML files
- Integrated Git Repositories
- Pipelines, Secrets, Approvals 

### Example YAML Pipeline - deploys an ARM Template

```
$ cat azure-pipelines.yml
# DevOps Pipeline Build file.
# The two RG_ variables are defined in the 'regular-variable-group'
# while the several AZURESPxxx (Service Principal) variables are defined
# in 'keyvault-variable-group' and get their values from my Azure Key Vault.
#
# Chris Joakim, Microsoft, 2019/11/11

trigger:
- master

pool:
  vmImage: 'Ubuntu 16.04'

variables:
- group: regular-variable-group
- group: keyvault-variable-group

steps:
- script: |
    echo 'RG_NAME:                '$(RG_NAME)
    echo 'RG_REGION:              '$(RG_REGION)
    echo 'AZURESPARMAPPID:        '$(AZURESPARMAPPID)
    echo 'AZURESPARMPASS:         '$(AZURESPARMPASS)
    echo 'AZURESPARMTENANT:       '$(AZURESPARMTENANT)
  displayName: 'display the pipeline variables; thekeyvault-variable-group values will appear as ***'
  condition: always()

- script: env | sort
  displayName: 'display environment variables'

- script: ls -alR
  displayName: 'list files'

- script: az login --service-principal --username $(AZURESPARMAPPID) --password $(AZURESPARMPASS) --tenant $(AZURESPARMTENANT)
  displayName: 'az login'

- script: az group create --name $(RG_NAME) --location $(RG_REGION)
  displayName: 'create resource group'

- script: |
    epoch_time=`date +%s`
    deployment_name=""$epoch_time"-storage-deployment"
    echo "deployment_name: "$deployment_name
    az group deployment create \
      --name $deployment_name \
      --resource-group $(RG_NAME) \
      --template-file storage-template.json \
      --parameters @storage-parameters.json
  displayName: 'create ARM deployment'
```
