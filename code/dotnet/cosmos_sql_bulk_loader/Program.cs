// Chris Joakim, Microsoft, September 2021

namespace CosmosBulkLoader {
    
    using System;
    using System.Collections.Generic;
    using System.Dynamic;
    using System.IO;
    using System.Linq;
    using System.Threading.Tasks;
    using Newtonsoft.Json;
    using Newtonsoft.Json.Converters;
    using Microsoft.Azure.Cosmos;

    class Program {
        private static string[] cliArgs = null;
        private static string   cliFunction = null;
        private static Config   config = null;
        private static CosmosClient cosmosClient = null;
        static async Task Main(string[] args) {
            if (args.Length < 1) {
                PrintCliExamples("Invalid command-line args");
                await Task.Delay(0);
                return;
            }

            cliArgs = args;
            config  = Config.Singleton(cliArgs);
            cliFunction = args[0];

            try {
                switch (cliFunction) {
                    case "list_databases":
                        await ListDatabases();
                        break;
                    case "create_database":
                        await CreateDatabase();
                        break;
                    case "update_database_throughput":
                        await UpdateDatabaseThroughput();
                        break;
                    case "delete_database":
                        await DeleteDatabase();
                        break;
                    case "list_containers":
                        await ListContainers();
                        break;
                    case "create_container":
                        await CreateContainer();
                        break;
                    case "update_container_throughput":
                        await UpdateContainerThroughput();
                        break;
                    case "update_container_indexing":
                        await UpdateContainerIndexing();
                        break;
                    case "truncate_container":
                        await TruncateContainer();
                        break;
                    case "delete_container":
                        await DeleteContainer();
                        break;
                    case "delete_route":
                        await DeleteRoute();
                        break;
                    case "bulk_load_container":
                        await BulkLoadContainer();
                        break;
                    case "count_documents":
                        await CountDocuments();
                        break;
                    case "execute_queries":
                        await ExecuteQueries();
                        break;
                    default:
                        PrintCliExamples($"invalid cliFunction: {cliFunction}");
                        break;
                }
            }
            catch (Exception e) {
                Console.WriteLine($"ERROR: Exception in Main() - ", e.Message);
                Console.WriteLine(e.StackTrace);
            }
            finally {
                if (cosmosClient != null) {
                    cosmosClient.Dispose();
                }
            }
            await Task.Delay(0);  // Task.Delay(0) ensures that the method is async
        }

        private static void PrintCliExamples(string msg) {
            if (msg != null) {
                Console.WriteLine($"Error: {msg}");
            }
            Console.WriteLine("");
            Console.WriteLine("Command-Line Examples:");
            Console.WriteLine("dotnet run list_databases");
            Console.WriteLine("dotnet run create_database <dbname> <shared-ru | 0>");
            Console.WriteLine("dotnet run delete_database <dbname>");
            Console.WriteLine("dotnet run update_database_throughput <dbname> <shared-ru>");
            Console.WriteLine("---");
            Console.WriteLine("dotnet run list_containers <dbname>");
            Console.WriteLine("dotnet run create_container <dbname> <cname> <pk> <ru>");
            Console.WriteLine("dotnet run update_container_throughput <dbname> <cname> <ru>");
            Console.WriteLine("dotnet run update_container_indexing <dbname> <cname> <json-doc-infile>");
            Console.WriteLine("dotnet run truncate_container <dbname> <cname>");
            Console.WriteLine("dotnet run delete_container <dbname> <cname>");
            Console.WriteLine("---");
            Console.WriteLine("dotnet run bulk_load_container <dbname> <cname> <json-rows-infile> <batch-count>");
            Console.WriteLine("dotnet run bulk_load_container dev travel data/air_travel_departures_10k.json 1");
            Console.WriteLine("---");
            Console.WriteLine("dotnet run count_documents <dbname> <cname>");
            Console.WriteLine("---");
            Console.WriteLine("dotnet run execute_queries <dbname> <cname> <queries-file>");
            Console.WriteLine("dotnet run delete_route <dbname> <cname> <route>");
            Console.WriteLine("dotnet run delete_route dev travel CLT:MBJ");
            Console.WriteLine("");
        }
        private static async Task ListDatabases() {
            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosAdminUtil util = new CosmosAdminUtil(cosmosClient, config.IsVerbose());
            List<string> dbList = await util.ListDatabases();
            Console.WriteLine($"ListDatabases - count {dbList.Count}");
            for (int i = 0; i < dbList.Count; i++) {
                string dbname = dbList[i];
                Database db = await util.GetDatabase(dbname);
                int? currentRU = await db.ReadThroughputAsync();
                if (currentRU == null) {
                    Console.WriteLine($"database {i+1}: {dbname} non-shared");
                }
                else {
                    Console.WriteLine($"database {i+1}: {dbname} current RU {currentRU}");
                }
            }
        }
        
        private static async Task CreateDatabase() {
            string dbname = cliArgs[1];
            int sharedRu = Int32.Parse(cliArgs[2]);
            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosAdminUtil util = new CosmosAdminUtil(cosmosClient, config.IsVerbose());
            DatabaseResponse resp = await util.CreateDatabase(dbname, sharedRu);
            Console.WriteLine(
                $"CreateDatabase {dbname} {sharedRu} -> status code {resp.StatusCode}, RU {resp.RequestCharge}");
        }

        private static async Task UpdateDatabaseThroughput() {
            string dbname = cliArgs[1];
            int sharedRu  = Int32.Parse(cliArgs[2]);
            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosAdminUtil util = new CosmosAdminUtil(cosmosClient, config.IsVerbose());
            int statusCode = await util.UpdateDatabaseThroughput(dbname, sharedRu);
            Console.WriteLine($"UpdateDatabaseThroughput {dbname} {sharedRu} -> statusCode {statusCode}");
        }
        private static async Task DeleteDatabase() {
            string dbname = cliArgs[1];
            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosAdminUtil util = new CosmosAdminUtil(cosmosClient, config.IsVerbose());
            int statusCode = await util.DeleteDatabase(dbname);
            Console.WriteLine($"DeleteDatabase {dbname} -> statusCode {statusCode}");  // 204 expected
        }

        private static async Task ListContainers() {
            string dbname = cliArgs[1];
            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosAdminUtil util = new CosmosAdminUtil(cosmosClient, config.IsVerbose());
            List<string> containerList = await util.ListContainers(dbname);
            Console.WriteLine($"ListContainers - count {containerList.Count}");
            for (int i = 0; i < containerList.Count; i++) {
                string cname = containerList[i];
                Console.WriteLine($"container in db: {dbname} -> {cname}");
            }
        }
        private static async Task CreateContainer() {
            string dbname = cliArgs[1];
            string cname  = cliArgs[2];
            string pk     = cliArgs[3];
            int    ru     = Int32.Parse(cliArgs[4]);
            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosAdminUtil util = new CosmosAdminUtil(cosmosClient, config.IsVerbose());
            string id = await util.CreateContainer(dbname, cname, pk, ru);
            Console.WriteLine($"CreateContainer {dbname} {cname} {ru} -> Id {id}"); 
        }
        
        private static async Task UpdateContainerThroughput() {
            string dbname = cliArgs[1];
            string cname  = cliArgs[2];
            int    ru     = Int32.Parse(cliArgs[3]);
            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosAdminUtil util = new CosmosAdminUtil(cosmosClient, config.IsVerbose());
            int statusCode = await util.UpdateContainerThroughput(dbname, cname, ru);
            Console.WriteLine($"UpdateContainerThroughput {dbname} {cname} {ru} -> statusCode {statusCode}");
        }
        
        private static async Task UpdateContainerIndexing() {
            string dbname = cliArgs[1];
            string cname  = cliArgs[2];
            string infile = cliArgs[3];
            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosAdminUtil util = new CosmosAdminUtil(cosmosClient, config.IsVerbose());
            // int statusCode = await util.UpdateContainerIndexing(dbname, cname, infile);
            // Console.WriteLine($"UpdateContainerThroughput {dbname} {cname} {ru} -> statusCode {statusCode}");
            await Task.Delay(0);
        }
        

        private static async Task TruncateContainer() {
            string dbname = cliArgs[1];
            string cname  = cliArgs[2];
            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosAdminUtil util = new CosmosAdminUtil(cosmosClient, config.IsVerbose());
            await util.SetCurrentDatabase(dbname);
            await util.SetCurrentContainer(cname);
            int deleteOperations = await util.TruncateContainer();
            Console.WriteLine($"TruncateContainer {dbname} {cname} -> deleteOperations {deleteOperations}");
        }
        
        private static async Task DeleteRoute() {
            string dbname = cliArgs[1];
            string cname  = cliArgs[2];
            string route  = cliArgs[3];
            cosmosClient  = CosmosClientFactory.RegularClient();
            CosmosQueryUtil util = new CosmosQueryUtil(cosmosClient, config.IsVerbose());
            await util.SetCurrentDatabase(dbname);
            await util.SetCurrentContainer(cname);
            string sql = $"select c.id, c.pk from c where c.route = '{route}'";
            
            QueryResponse respObj = await util.ExecuteQuery(sql);
            string jstr = respObj.ToJson();
            string outfile = "out/delete_route.json";
            await File.WriteAllTextAsync(outfile, jstr);
            Console.WriteLine($"file written: {outfile}");

            for (int i = 0; i < respObj.itemCount; i++) {
                dynamic item = respObj.items[i];
                string id = item["id"];
                string pk = item["pk"];
                GenericDocument gd = new GenericDocument(id, pk);
                Console.WriteLine($"deleting {gd.ToJson()}");
                ItemResponse<GenericDocument> resp = await util.DeleteGenericDocument(gd);
                Console.WriteLine($"resp, status: {resp.StatusCode} ru: {resp.RequestCharge}");
            }
        }
        
        private static async Task DeleteContainer() {
            string dbname = cliArgs[1];
            string cname  = cliArgs[2];
            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosAdminUtil util = new CosmosAdminUtil(cosmosClient, config.IsVerbose());
            int statusCode = await util.DeleteContainer(dbname, cname);
            Console.WriteLine($"DeleteContainer {dbname} {cname} -> statusCode {statusCode}");
        }
        
        private static async Task BulkLoadContainer() {
            string dbname   = null;
            string cname    = null;
            string infile   = null;
            int    maxBatchCount = 0;
            int    batchSize  = 500;
            int    batchCount = 0;
            int    taskCount  = 0;
            long   startEpoch = 0;
            int    exceptions = 0;
            
            try {
                dbname   = cliArgs[1];
                cname    = cliArgs[2];
                infile   = cliArgs[3];
                maxBatchCount = Int32.Parse(cliArgs[4]);
                
                Console.WriteLine($"dbname:   {dbname}");
                Console.WriteLine($"cname:    {cname}");
                Console.WriteLine($"infile:   {infile}");
                Console.WriteLine($"mbc:      {maxBatchCount}");

                cosmosClient = CosmosClientFactory.BulkLoadingClient();
                Database  database  = cosmosClient.GetDatabase(dbname);
                Container container = database.GetContainer(cname);
                List<Task> tasks = new List<Task>(batchSize);
                Console.WriteLine(
                    $"LoadContainer - db: {dbname}, container: {cname}, infile: {infile}, maxBatchCount: {maxBatchCount}");
                startEpoch = EpochMsTime();

                using (FileStream fs = File.Open(infile, FileMode.Open, FileAccess.Read, FileShare.ReadWrite)) {
                    using (BufferedStream bs = new BufferedStream(fs)) {
                        using (StreamReader sr = new StreamReader(bs)) {
                            string jsonLine;
                            while ((jsonLine = sr.ReadLine()) != null) {
                                if (batchCount < maxBatchCount) {
                                    // Parse the JSON line into a "dynamic" object, like a python dict
                                    dynamic jsonDoc = JsonConvert.DeserializeObject<ExpandoObject>(
                                        jsonLine.Trim(), new ExpandoObjectConverter());
                                    // jsonDoc is an instance of class System.Dynamic.ExpandoObject (dynamic)
                                    
                                    // Set some additional attributes on the dynamic jsonDoc
                                    DateTimeOffset now = DateTimeOffset.UtcNow;
                                    jsonDoc.doc_epoch = now.ToUnixTimeMilliseconds();
                                    jsonDoc.doc_time = now.ToString("yyyy/MM/dd-HH:mm:ss");
                                    jsonDoc.id = Guid.NewGuid().ToString();
                                    
                                    // Add an UpsertItemAsync task to the list of tasks for a batch
                                    tasks.Add(container.UpsertItemAsync(jsonDoc, new PartitionKey(jsonDoc.pk)));
                                    taskCount++;

                                    if (tasks.Count == batchSize) {
                                        // Display the last jsonDoc in this batch
                                        Console.WriteLine(JsonConvert.SerializeObject(jsonDoc));
                                        
                                        batchCount++;
                                        Console.WriteLine($"writing batch {batchCount} ({tasks.Count}) at {EpochMsTime()}");
                                        
                                        // execute all of the Tasks in this batch, and await them
                                        await Task.WhenAll(tasks);
                                        
                                        // reset the tasks list to an empty list for the next batch
                                        tasks = new List<Task>(batchSize);
                                    }
                                }
                                else {
                                    return;
                                }
                            }
                        }
                    }
                }
                if (tasks.Count > 0) {
                    // execute the last batch if there are any tasks
                    batchCount++;
                    Console.WriteLine($"writing batch {batchCount} ({tasks.Count}) at {EpochMsTime()}");
                    await Task.WhenAll(tasks);
                }
            }
            catch (Exception e) {
                Console.WriteLine($"EXCEPTION: {e.Message}");
                exceptions++;
                throw;
            }
            finally {
                long finishEpoch = EpochMsTime();
                long elapsedMs = finishEpoch - startEpoch;
                double elapsedSec = (double) elapsedMs / (double) 1000;
                double elapsedMin = elapsedSec / (double) 60.0;
                double docsPerSec = taskCount / elapsedSec;
                Console.WriteLine("");
                Console.WriteLine("EOJ Totals:");
                Console.WriteLine($"  Database:             {dbname}");
                Console.WriteLine($"  Container:            {cname}");
                Console.WriteLine($"  Input Filename:       {infile}");
                Console.WriteLine($"  Max Batch Count:      {maxBatchCount}");
                Console.WriteLine($"  BulkLoad startEpoch:  {startEpoch}");
                Console.WriteLine($"  BulkLoad finishEpoch: {finishEpoch}");
                Console.WriteLine($"  BulkLoad elapsedMs:   {elapsedMs}");
                Console.WriteLine($"  BulkLoad elapsedSec:  {elapsedSec}");
                Console.WriteLine($"  BulkLoad elapsedMin:  {elapsedMin}");
                Console.WriteLine($"  Batch Size:           {batchSize}");
                Console.WriteLine($"  Batch Count:          {batchCount}");
                Console.WriteLine($"  Exceptions:           {exceptions}");
                Console.WriteLine($"  Document/Task count:  {taskCount}");
                Console.WriteLine($"  Document per Second:  {docsPerSec}");
                Console.WriteLine("");
            }
            await Task.Delay(0);
        }
        
        private static async Task CountDocuments() {
            string dbname = cliArgs[1];
            string cname  = cliArgs[2];
            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosQueryUtil util = new CosmosQueryUtil(cosmosClient, config.IsVerbose());
            await util.SetCurrentDatabase(dbname);
            await util.SetCurrentContainer(cname);
            int count = (await util.CountDocuments("")).items[0];
            Console.WriteLine($"CountDocuments {dbname} {cname} -> {count}"); 
        }

        private static async Task ExecuteQueries() {
            string dbname = cliArgs[1];
            string cname  = cliArgs[2];
            string infile = cliArgs[3];

            cosmosClient = CosmosClientFactory.RegularClient();
            CosmosQueryUtil util = new CosmosQueryUtil(cosmosClient, config.IsVerbose());
            await util.SetCurrentDatabase(dbname);
            await util.SetCurrentContainer(cname);

            // Console.WriteLine("warming sdk client...");
            for (int i = 0; i < 2; i++) {
                await util.CountDocuments("");
            }
            
            foreach (string line in File.ReadLines(infile)) {
                string[] tokens = line.Split("|");
                if (tokens.Length > 1) {
                    string qname = tokens[0].Trim();
                    string sql   = tokens[1].Trim();
                    if (qname.StartsWith("q")) {
                        Console.WriteLine("");
                        Console.WriteLine("================================================================================");
                        Console.WriteLine($"executing qname: {qname}, db: {dbname}, cname: {cname}, sql: {sql}");
                        QueryResponse respObj = await util.ExecuteQuery(sql);
                        respObj.queryName = qname;
                        respObj.sql = sql;
                        respObj.dbname = dbname;
                        respObj.cname  = cname;
                        respObj.Finish();
                        Console.WriteLine(respObj.ToString());
                        string jstr = respObj.ToJson();
                        if (config.IsVerbose()) {
                            Console.WriteLine(jstr);
                        }
                        await File.WriteAllTextAsync(respObj.filename, jstr);
                        Console.WriteLine($"file written: {respObj.filename}");
                    }  
                }
            }
        }
        /**
         * Use the cosmosClient to "warm it up" before starting a timed performance test.
         */
        private static async Task WarmupClient(string dbname, string cname) {
            CosmosAdminUtil util = new CosmosAdminUtil(cosmosClient, config.IsVerbose());
            List<string> containerList = await util.ListContainers(dbname);
            Console.WriteLine($"ListContainers - count {containerList.Count}");
            for (int i = 0; i < containerList.Count; i++) {
                string name = containerList[i];
                if (name.Equals(cname)) {
                    Console.WriteLine($"OK: container {cname} is present in db: {dbname}"); 
                }
            }
        }

        private static long EpochMsTime() {
            return new DateTimeOffset(DateTime.UtcNow).ToUnixTimeMilliseconds();
        }
    }
}