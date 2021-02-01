using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using Microsoft.Azure.Documents;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Extensions.Logging;

using Microsoft.Azure.Cosmos;

/**
 * Authors: Theo van Kraay & Chris Joakim, Microsoft, June 2020 
 */

namespace CosmosSqlChangeFeedV3
{
    public static class CosmosSqlChangeFeedV3
    {
        // Environment Variable:                Example Value:
        // AZURE_COSMOSDB_SQLDB_CONN_STRING     <your-cosmosdb-connection-string>

        private static readonly string databaseId = "dev";
        private static readonly string outputContainerId = "changes";
        private static readonly string connString =
            System.Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_CONN_STRING");

        private static CosmosClient cosmosClient = new CosmosClient(connString);

        [FunctionName("CosmosSqlChangeFeedV3")]
        public static async Task Run([CosmosDBTrigger(
            databaseName: "dev",
            collectionName: "events",
            ConnectionStringSetting = "AZURE_COSMOSDB_SQLDB_CONN_STRING",
            LeaseCollectionName = "leases",
            CreateLeaseCollectionIfNotExists = true)] IReadOnlyList<Document> inputList, ILogger log)
        {
            // Use the Microsoft.Azure.Cosmos SDK to write to the output/changes container.
            var outputContainer = cosmosClient.GetContainer(databaseId, outputContainerId);

            foreach (Document doc in inputList)
            {
                try
                {
                    // Capture the Id of the source document and generate a new Id for the output doc
                    // so as to handle both inserts and updates.
                    var originalId = doc.Id;
                    doc.SetPropertyValue("_originalId", originalId);
                    doc.SetPropertyValue("id", Guid.NewGuid().ToString());
                    await outputContainer.CreateItemAsync<Document>(doc);
                    log.LogInformation("doc saved to outputContainer with originalId: " + originalId);
                }
                catch (Exception e)
                {
                    log.LogError("Exception pushing doc outputContainer: " + e);
                    log.LogError("doc NOT saved to outputContainer: " + doc);
                    throw e;  // Terminate the Function invocation unsuccessfully.
                }
            }
        }
    }
}
