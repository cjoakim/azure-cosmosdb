
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

using Microsoft.Azure.Cosmos;

using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

// dotnet run dev sales data/x1.json preview
// dotnet run dev airports data/x1.json preview
// dotnet run dev airports data/x1.json upsert

namespace json_loader
{
    class Program
    {
        // Constants:
        public const string standardPartitionKeyName = "/pk";

        // Class variables:
        private static CosmosClient client = null;
        private static Database db = null;
        private static Container container = null;

        static async Task Main(string[] args)
        {
            Console.WriteLine($"command-line args length: {args.Length}");

            if (args.Length > 2)
            {
                string targetDB   = args[0];
                string targetColl = args[1];
                string infile     = args[2];
                string doUpserts  = args[3].ToLower();

                // I personally use these environment variables as a personal convention;
                // this is not an Azure or SDK standard.
                string uriEnvVar  = "AZURE_COSMOSDB_SQLDB_URI";
                string keyEnvVar  = "AZURE_COSMOSDB_SQLDB_KEY";

                // You can optionally pass in the names of YOUR environment variables instead.
                if (args.Length > 5)
                {
                    uriEnvVar = args[4];
                    keyEnvVar = args[5];
                }

                // string connStrEnvVar = args[2];
                Console.WriteLine($"infile:     {infile}");
                Console.WriteLine($"targetDB:   {targetDB}");
                Console.WriteLine($"targetColl: {targetColl}");
                Console.WriteLine($"uriEnvVar:  {uriEnvVar}");
                Console.WriteLine($"keyEnvVar:  {keyEnvVar}");

                string uri = Environment.GetEnvironmentVariable(uriEnvVar);
                string key = Environment.GetEnvironmentVariable(keyEnvVar);
                Console.WriteLine($"uri:        {uri}");
                Console.WriteLine($"key:        {key}");

                JArray documentArray = ReadJsonInfile(infile);
                int counter = 0;

                await ConnectToCosmos(uri, key, targetDB, targetColl);

                foreach (JObject doc in documentArray)
                {
                    counter++;
                    // Console.WriteLine($"doc type {doc.GetType().Name}");

                    // Get some values from the JSON document
                    string firstName = doc.GetValue("FirstName").ToString();
                    string lastName  = doc.GetValue("LastName").ToString();
                    string partitionKey = $"{lastName}, {firstName}";

                    // Add some values to the JSON document
                    doc.Add("Seq", new JValue(counter));
                    doc.Add("pk", new JValue(partitionKey));

                    Guid g = Guid.NewGuid();
                    doc.Add("id", Guid.NewGuid().ToString());

                    // Remove some values from the JSON document
                    doc.Remove("PasswordHash");
                    doc.Remove("PasswordSalt");

                    // Display the document as JSON
                    Console.WriteLine(doc);

                    if (doUpserts == "upsert")
                    {
                        // Microsoft.Azure.Cosmos.ItemResponse`1[Newtonsoft.Json.Linq.JObject]
                        Console.WriteLine(await container.CreateItemAsync(doc, new PartitionKey(partitionKey)));
                    }
                }
            }
            else
            {
                Console.WriteLine("ERROR; invalid command-line args.  See Program.cs Main method.");
            }

            await Task.Delay(0);  // required initially as Main has no async calls

        }

        /**
         * The contents of the given infile are expected to be a JSON Array, not JSON Object.
         * For example, the JSON begins and ends with [] rather than {}.
         */
        private static JArray ReadJsonInfile(string infile)
        {
            string jsonText = System.IO.File.ReadAllText(infile);
            JArray array = JArray.Parse(jsonText);  
            Console.WriteLine($"jsonText read; length: {jsonText.Length}  element count: {array.Count}");
            // jsonText read; length: 463427  element count: 847
            return array;
        }

        static async Task ConnectToCosmos(string uri, string key, string dbName, string collName)
        {
            Console.WriteLine("ConnectToCosmos...");

            CosmosClientOptions options = new CosmosClientOptions
            {
                AllowBulkExecution = false
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
