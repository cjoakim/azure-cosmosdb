using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Azure.Cosmos;

// https://docs.microsoft.com/en-us/azure/cosmos-db/change-feed-processor#where-to-host-the-change-feed-processor

namespace ChangeFeedConsole
{
    class Program
    {
        private static readonly string _endpointUrl = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_URI");
        private static readonly string _primaryKey  = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_KEY");
        private static readonly string _databaseId  = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_DBNAME");
        private static readonly string _containerId = "cart";

        private static readonly string _destinationContainerId = "cartChanges";

        static async Task Main(string[] args)
        {
            using (var client = new CosmosClient(_endpointUrl, _primaryKey))
            {
                var db = client.GetDatabase(_databaseId);
                var container = db.GetContainer(_containerId);
                var destinationContainer = db.GetContainer(_destinationContainerId);

                Container leaseContainer = 
                    await db.CreateContainerIfNotExistsAsync(
                        id: "cartLeases", partitionKeyPath: "/id", throughput: 400);

                var builder = container.GetChangeFeedProcessorBuilder(
                    "migrationProcessor", (IReadOnlyCollection<CartAction> input, 
                    CancellationToken cancellationToken) =>
                {
                    Console.WriteLine(input.Count + " Changes Received");

                    var tasks = new List<Task>();
                    foreach (var doc in input)
                    {
                        tasks.Add(destinationContainer.CreateItemAsync(
                            doc, new PartitionKey(doc.BuyerState)));
                    }
                    return Task.WhenAll(tasks);
                });

                var processor = builder
                    .WithInstanceName("changeFeedConsole")
                    .WithLeaseContainer(leaseContainer).Build();

                await processor.StartAsync();

                Console.WriteLine("Started Change Feed Processor");
                Console.WriteLine("Press any key to stop the processor...");
                Console.ReadKey();
                Console.WriteLine("Stopping Change Feed Processor");

                await processor.StopAsync();
            }
        }
    }
}