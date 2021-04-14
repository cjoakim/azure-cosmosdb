# Enable Synapse Link for CMK

## Links

- https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-setup-cmk
- https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-setup-managed-identity
- https://docs.microsoft.com/en-us/azure/cosmos-db/synapse-link#security

---

## Steps

### 1 - Create System Identity for CosmosDB

First, you will need to create system identity for Cosmos DB account, to enable CMK for analytical store.  First party identity will not work.

Instructions to create managed identity:
https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-setup-managed-identity

### 2 - Add Identity to Key Vault Access Policy

Once you create the managed identity you will need to add this to key vault access policy,
change the identity type on the account to system identity.

### 3 - Turn on Synapse Link

You can then turn on Synapse Link for this account/containers.

https://docs.microsoft.com/en-us/azure/cosmos-db/synapse-link#security
