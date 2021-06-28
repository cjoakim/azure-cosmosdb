# 1.01 - Azure


## IaaS

**Infrastructure-as-a-Service** 

- Servers, Storage, and Networking
- Low-level 
- Burden is on the Customer to deploy, patch, integrate, secure, scale

See https://azure.microsoft.com/en-us/overview/what-is-azure/iaas/

---

## PaaS

**Platform-as-a-Service** 

- Completely Managed by the Cloud Provider
- "Serverless"
- Scalable
- **CosmosDB is PaaS**
- Azure App Service, Azure Synapse, Azure EventHubs, etc. are PaaS

See https://azure.microsoft.com/en-us/overview/what-is-paas/

---

## Advantages of Cloud

- Provisioning Model
- On-demand Scalability
- No on-site hardware required
- Cost-effective Subscription model
- High availability, SLAs
- Enterprise-level development tools
- World-class Cybersecurity
- Advanced Compliance features

See https://www.actsolution.net/blog/what-are-the-business-benefits-of-microsoft-azure-cloud/

--

## Azure Regions

Locate your Azure Services close to your customers.  Replication.

<p align="center"><img src="img/azure-regions-map.svg" width="80%"></p>

--- 

## Azure High-Speed Fiber Network

<p align="center"><img src="img/azure-network-map.svg" width="80%"></p>

---

**CosmosDB is a "ring 0" service available in all reqions.**

- https://azure.microsoft.com/en-us/global-infrastructure/

--

## Hierarchy

Azure uses this hierarchy for cost and RBAC isolation.

```
Enterprise Agreement
    Subscription 1
        Resource Group 1
           ...resources.
           ...CosmosDB
        Resource Group 2
           ...resources.
        Resource Group n
           ...resources.

        Resource Group App XYZ Dev
           ...resources
           ...Dev CosmosDB
        Resource Group App XYZ QA
           ...resources
           ...QA CosmosDB
        Resource Group App XYZ Prod
           ...resources
           ...Prod CosmosDB

    Subscription n
        Resource Group 1
           ...resources.
        Resource Group 2
           ...resources.
        Resource Group n
           ...resources.
           ...another CosmosDB
           ...another CosmosDB
```

See https://docs.microsoft.com/en-us/azure/cloud-adoption-framework/decision-guides/subscriptions/

---

## Pets vs Cattle

<p align="center"><img src="img/pets-vs-cattle.png" width="80%"></p>

Pets are your on-prem servers you've know for years.  Lots of care-and-feeding.

Cattle are IaaS resources and PaaS services you can quickly consume and dispose of.

See http://cloudscaling.com/blog/cloud-computing/the-history-of-pets-vs-cattle/

---

## Provisioning Azure Resources

- Manually in the Azure Portal Web UI (https://portal.azure.com/)
- [Azure PowerShell cmdlets](https://docs.microsoft.com/en-us/powershell/azure/?view=azps-6.1.0)
- [az CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Azure Resource Manager (ARM) Templates](https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/overview)
- [Bicep](https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview)
- Azure Programming Language SDKs (DotNet, Java, Python, Node.js, etc.)
- [Terraform](https://docs.microsoft.com/en-us/azure/developer/terraform/overview)

See https://docs.microsoft.com/en-us/azure/developer/python/cloud-development-provisioning

See the **automation/** directory of this repo.

### az CLI example - create a Resource Group, with CosmosDB

```
    az group create \
        --location $cosmos_sql_region \
        --name $cosmos_sql_rg \
        --subscription $subscription

    az cosmosdb create \
        --name $cosmos_sql_acct_name \
        --resource-group $cosmos_sql_rg \
        --subscription $subscription \
        --locations regionName=$cosmos_sql_region failoverPriority=0 isZoneRedundant=False \
        --default-consistency-level $cosmos_sql_acct_consistency \
        --enable-multiple-write-locations true \
        --enable-analytical-storage true \
        --kind $cosmos_sql_acct_kind
```

---

## DevOps

> DevOps is a set of practices that combines software development (Dev) and IT operations (Ops).
> It aims to shorten the systems development life cycle and provide continuous delivery with high software quality.
> DevOps is complementary with Agile software development; several DevOps aspects came from the Agile methodology.

- [Wikipedia](https://en.wikipedia.org/wiki/DevOps)
- [Azure DevOps](https://azure.microsoft.com/en-us/services/devops/): boards, repos, pipelines, artifacts, testing

---

## Security & Compliance

### Pervasive Features

- Encryption at Rest
- Encryption in Flight
- Azure Active Directory (AAD) and RBAC
- AI-driven Monitoring based on our vast history

### Links

- https://azure.microsoft.com/en-us/overview/trusted-cloud/compliance/
- https://docs.microsoft.com/en-us/azure/compliance/
- [Advanced Threat Protection (ATP)](https://techcommunity.microsoft.com/t5/security-compliance-and-identity/introducing-azure-advanced-threat-protection/ba-p/250332)

---

## Marketplace

> Search from a rich catalog of more than **17,000 certified apps and services**, deploy seamlessly, and simplify billing with a single bill for all Microsoft and third-party solutions.

See Azure Portal.

See https://azure.microsoft.com/en-us/marketplace/

---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](0_table_of_contents.md) &nbsp; | &nbsp; [next](1_02_nosql.md) &nbsp;
