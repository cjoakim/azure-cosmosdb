using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Azure.Documents;
using Microsoft.Azure.WebJobs;
using Microsoft.Azure.WebJobs.Host;
using Microsoft.Extensions.Logging;

// Implementation of an Azure Function triggered by CosmosDB/Gremlin Change-Feed events.
// Chris Joakim, Microsoft, 2021/01/21

namespace CosmosGremlinTrigger
{
    public static class CosmosGremlinTrigger
    {
        [FunctionName("CosmosGremlinTrigger")]
        public static void Run([CosmosDBTrigger(
            databaseName: "dev",
            collectionName: "npm",
            ConnectionStringSetting = "AZURE_COSMOSDB_GRAPHDB_CONN_STRING",
            CreateLeaseCollectionIfNotExists = true,
            LeaseCollectionName = "leases")]IReadOnlyList<Document> input, ILogger log)
        {
            if (input != null && input.Count > 0)
            {
                log.LogInformation("Documents modified " + input.Count);
                var options = new JsonSerializerOptions
                {
                    WriteIndented = true,
                };

                foreach (var item in input)
                {
                    log.LogInformation("Document Id " + item.Id);
                    log.LogInformation(JsonSerializer.Serialize(item, options));
                }
            }
        }
    }
}
