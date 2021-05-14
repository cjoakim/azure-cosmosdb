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
            
            RequestOptions requestOptions = new RequestOptions();

            int? dbThroughput = await db.ReadThroughputAsync();
            if (dbThroughput == null)
            {
                Console.WriteLine($"dbThroughput is null");
            }
            else
            {
                Console.WriteLine($"dbThroughput: {dbThroughput}");
            }

            int? containerThroughput = await container.ReadThroughputAsync();
            if (containerThroughput == null)
            {
                Console.WriteLine($"containerThroughput is null");
            }
            else
            {
                Console.WriteLine($"containerThroughput: {containerThroughput}");
            }
            
            
            //await Task.Delay(0);
        }
        
        private static async Task Tasks()
        {
            Console.WriteLine("Tasks");

            int batchCount = 5;
            int taskCount  = 10;
            Random random = new Random();
            List<Task> tasks = null;

            for (int b = 0; b < batchCount; b++)
            {
                long startTime = EpochMsTime();
                Console.WriteLine($"batch {b} adding tasks at {startTime}");
                tasks = new List<Task>();
                for (int t = 0; t < taskCount; t++)
                {
                    int ms = random.Next(3000, 5000);
                    Console.WriteLine($"batch {b} adding task {ms}");
                    tasks.Add(Task.Delay(ms));
                }
                await Task.WhenAll(tasks.ToArray());
                long finishTime = EpochMsTime();
                Console.WriteLine($"batch {b} finished tasks at {finishTime} ({finishTime - startTime})");
                foreach (Task task in tasks)
                {
                    Console.WriteLine($"  task status {task.Id} {task.Status}");
                    // https://docs.microsoft.com/en-us/dotnet/api/system.threading.tasks.taskstatus?view=net-5.0

                    switch (task.Status)
                    {
                        case TaskStatus.Canceled:
                            Console.WriteLine($"  task status cancelled {task.Id} {task.Status}");
                            break;
                        case TaskStatus.Faulted:
                            Console.WriteLine($"  task status faulted {task.Id} {task.Status}");
                            break;
                        default:
                            Console.WriteLine($"  task status ok {task.Id} {task.Status}");
                            break;      
                    }
                }
            }
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

            container = db.GetContainer(collName);
            //container = await db.CreateContainerIfNotExistsAsync(collName, standardPartitionKeyName);
            Console.WriteLine("connected to container: {0}", container.Id);
        }
        
        private static long EpochMsTime()
        {
            return new DateTimeOffset(DateTime.UtcNow).ToUnixTimeMilliseconds();
        }
    }
}
