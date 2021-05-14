using System;

using System.Collections.Generic;
using System.IO;
using System.Globalization;
using System.Threading.Tasks;
using Newtonsoft.Json;

using Microsoft.Azure.Cosmos;

namespace account_explorer
{
    class Program
    {
        // Class variables:
        private static Config config = null;
        private static CosmosClient client = null;
        private static Database     db = null;
        private static Container    container = null;
        public const string standardPartitionKeyName = "/pk";
        
        private static void DisplayCliOptions(string msg)
        {
            Console.WriteLine("");
            Console.WriteLine("Command-Line Options:");
            if (msg != null) {
                Console.WriteLine($"ERROR: {msg}");
            }
            Console.WriteLine("$ dotnet run throughput <db> <container>");
            Console.WriteLine("");
        }
        
        static async Task Main(string[] args)
        {
            config = new Config(args);
            
            switch (config.FirstArg())
            {
                case "throughput":
                    await Throughput();
                    break;
                case "tasks":
                    await Tasks();
                    break;
                default:
                    Console.WriteLine("Invalid Config: unknown command-line function {0}", config.FirstArg());
                    return;
            }
        }

        private static async Task Throughput()
        {
            Console.WriteLine("Throughput");
            await ConnectToCosmos(false);
            
             
            await Task.Delay(0);
        }
        
        private static async Task Tasks()
        {
            Console.WriteLine("Tasks");
            await Task.Delay(0);
        }
        
        static async Task ConnectToCosmos(bool allowBulk)
        {
            string uri = config.GetCosmosUri();
            string key = config.GetCosmosKey();
            string dbName = config.GetCliKeywordArg("--db");
            string collName = config.GetCliKeywordArg("--coll");
            
            Console.WriteLine("ConnectToCosmos...");
            Console.WriteLine($"uri:         {uri}");
            Console.WriteLine($"key:         {key.Length}");
            Console.WriteLine($"dbName:      {dbName}");
            Console.WriteLine($"collName:    {collName}");

            CosmosClientOptions options = new CosmosClientOptions {
                //AllowBulkExecution = allowBulk
                //ConnectionMode = ConnectionMode.Gateway // ConnectionMode.Direct is the default
            };
            client = new CosmosClient(uri, key, options);
            Console.WriteLine("client {0}", client);

            db = await client.CreateDatabaseIfNotExistsAsync(dbName);
            Console.WriteLine("connected to db: {0}", db.Id);

            container = await db.CreateContainerIfNotExistsAsync(collName, standardPartitionKeyName);
            Console.WriteLine("connected to container: {0}", container.Id);
        }
    }
}
