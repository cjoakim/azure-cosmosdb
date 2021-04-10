using System;

using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.IO;
using System.Text.Json;
using System.Threading.Tasks;

using Microsoft.Azure.Cosmos;

using CsvHelper;
using CsvHelper.Configuration;

using Newtonsoft.Json;

// Chris Joakim, Microsoft, 2021/04/10

namespace CJoakim.Cosmos.CompIdx
{
    public class Program
    {
        // Constants:
        public const string standardPartitionKeyName = "/pk";

        // Class variables:
        private static string       cliFunction = null;
        private static string       uri = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_URI");
        private static string       key = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_KEY");
        private static string       dbName = "compidx";
        private static string       collName = "coll2";
        private static string       queryName = null;
        private static CosmosClient client = null;
        private static Database     db = null;
        private static Container    container = null;
        private static string       continuationToken = null;

        static async Task Main(string[] args)
        {
            if (args.Length > 0) {
                cliFunction = args[0];
                Console.WriteLine($"args:        {JsonConvert.SerializeObject(args)}");
                Console.WriteLine($"cliFunction: {cliFunction}");

                switch (cliFunction) {             
                    case "read_display_csv": 
                        await ReadDisplayCsv();
                        break; 
                    case "bulk_load": 
                        dbName = args[1];
                        collName = args[2];
                        await BulkLoad();
                        break; 
                    case "query": 
                        dbName = args[1];
                        collName = args[2];
                        queryName = args[3];
                        await Query();
                        break; 
                    default: 
                        DisplayCliOptions($"Unknown cliFunction: {cliFunction}");
                        break; 
                }
                if (client != null) {
                    client.Dispose();
                    Console.WriteLine("client disposed");
                }
                return;
            }
            else {
                DisplayCliOptions("Invalid command-line args");
                return;
            }
        }

        private static void DisplayCliOptions(string msg)
        {
            Console.WriteLine("");
            Console.WriteLine("DisplayCliOptions:");
            if (msg != null) {
                Console.WriteLine($"Error: {msg}");
            }
            Console.WriteLine("$ dotnet run read_display_csv");
            Console.WriteLine("");
            Console.WriteLine("$ dotnet run <cliFunction> <dbName> <collName> <other args...>");
            Console.WriteLine("$ dotnet run bulk_load compidx coll1");
            Console.WriteLine("$ dotnet run bulk_load compidx coll2");
            Console.WriteLine("");
            Console.WriteLine("$ dotnet run query compidx coll1 <query_name>");
            Console.WriteLine("$ dotnet run query compidx coll1 count_documents");
            Console.WriteLine("$ dotnet run query compidx coll2 montpelier");
            Console.WriteLine("$ dotnet run query compidx coll2 vermont_noindex_ordered");
            Console.WriteLine("$ dotnet run query compidx coll2 vermont_index_ordered");
            
            Console.WriteLine("");
        }

        static async Task ConnectToCosmos(bool allowBulk)
        {
            Console.WriteLine("ConnectToCosmos...");
            Console.WriteLine($"uri:         {uri}");
            Console.WriteLine($"key:         {key}");
            Console.WriteLine($"dbName:      {dbName}");
            Console.WriteLine($"collName:    {collName}");

            CosmosClientOptions options = new CosmosClientOptions {
                AllowBulkExecution = allowBulk
            };
            client = new CosmosClient(uri, key, options);
            Console.WriteLine("client {0}", client);

            db = await client.CreateDatabaseIfNotExistsAsync(dbName);
            Console.WriteLine("connected to db: {0}", db.Id);

            container = await db.CreateContainerIfNotExistsAsync(collName, standardPartitionKeyName);
            Console.WriteLine("connected to container: {0}", container.Id);
        }

        static async Task ReadDisplayCsv()
        {
            long startEpoch = EpochMsTime();
            List<PostalCode> postalCodes = ReadPostalCodesCsv();
            foreach (var obj in postalCodes)
            {
                Console.WriteLine(obj.ToJson());
            }
            long finishEpoch = EpochMsTime();
            double elapsedTime = (finishEpoch - startEpoch) / 1000.0;
            Console.WriteLine("elapsedTime: {0}", elapsedTime);
            await Task.Delay(0);
        }

        static async Task BulkLoad()
        {
            await ConnectToCosmos(true);
            
            List<PostalCode> postalCodes = ReadPostalCodesCsv();
            List<Task> tasks  = new List<Task>(postalCodes.Count);
            int responseCount = 0;
            long startEpoch   = EpochMsTime();

            foreach (PostalCode item in postalCodes)
            {
                tasks.Add(container.CreateItemAsync(item, new PartitionKey(item.pk))
                    .ContinueWith(itemResponse =>
                    {
                        responseCount++;

                        if (itemResponse.IsCompletedSuccessfully)
                        {
                            Console.WriteLine("successful {0} {1} {2} {3}",
                                responseCount,
                                itemResponse.Result.StatusCode,
                                itemResponse.Result.RequestCharge,
                                itemResponse.Result.Resource.ToJson());
                        }
                        else
                        {
                            Console.WriteLine("exception  {0} {1}", responseCount, itemResponse.Exception);
                        }
                    }));
            }

            Console.WriteLine("Tasks created; awaiting completion...");
            await Task.WhenAll(tasks);  // Wait until all are done

            long finishEpoch = EpochMsTime();
            double elapsedTime = (finishEpoch - startEpoch) / 1000.0;
            Console.WriteLine("Tasks completed in {0} seconds", elapsedTime);
        }

        static async Task Query()
        {
            Dictionary<string, string> namedQueries = new Dictionary<string, string>();
            namedQueries.Add("count_documents", "SELECT COUNT(1) FROM c");
            namedQueries.Add("select_two",  "SELECT * from c where c.pk = 'CA' and CONTAINS(c.cityName, 'San') order by c.cityName");
            namedQueries.Add("select_four", "SELECT * from c where c.stateAbbrv = 'CA' and CONTAINS(c.cityName, 'San') and c.longitude < 117 and c.latitude < 38.0 order by c.pk");
            namedQueries.Add("select_four_ordered_two", "SELECT * from c where c.stateAbbrv = 'CA' and CONTAINS(c.cityName, 'San') and c.longitude < 117 and c.latitude < 38.0 order by c.pk, c.cityName");
            namedQueries.Add("davidson_geo", "SELECT * from c WHERE ST_DISTANCE(c.location, {'type': 'Point', 'coordinates':[-80.7978540000,35.4833060000]}) <= 10000");

            if (namedQueries.ContainsKey(queryName))
            {
                await ConnectToCosmos(true);
                string sql = namedQueries[queryName];

                List<dynamic> items = await ExecuteQuery(sql, 1000);
                for (int i = 0; i < items.Count; i++)
                {
                    Console.WriteLine(items[i]);
                }
            }
            else
            {
                Console.WriteLine("Undefined named query: {0}", queryName);
            }
            

            await Task.Delay(0);
        }


        static async Task<List<dynamic>> ExecuteQuery(string sql, int maxItems=1000)
        {
            Console.WriteLine($"ExecuteQuery - sql: {sql}");
            double totalRequestCharge = 0;
            List<dynamic> items = new List<dynamic>();

            QueryDefinition queryDefinition = new QueryDefinition(sql);
            QueryRequestOptions requestOptions = new QueryRequestOptions()
            {
                MaxItemCount = maxItems
            };

            FeedIterator<dynamic> queryResultSetIterator = 
                container.GetItemQueryIterator<dynamic>(queryDefinition, requestOptions: requestOptions);

            while (queryResultSetIterator.HasMoreResults)
            {
                FeedResponse<dynamic> feedResponse =
                    await queryResultSetIterator.ReadNextAsync();
                if (feedResponse.ContinuationToken != null)
                {
                    continuationToken = feedResponse.ContinuationToken;
                    Console.WriteLine($"ExecuteQuery - continuationToken: {continuationToken}");
                }
                totalRequestCharge += feedResponse.RequestCharge;
                foreach (var item in feedResponse)
                {
                    items.Add(item);
                }
            }
            Console.WriteLine($"ExecuteQuery - result count: {items.Count}, RU: {totalRequestCharge}");
            return items;
        }

        private static List<PostalCode> ReadPostalCodesCsv()
        {
            // See https://joshclose.github.io/CsvHelper/getting-started/#reading-a-csv-file

            List<PostalCode> postalCodes = new List<PostalCode>();
            try
            {
                string infile = AbsolutePath("data/postal_codes_us_filtered.csv");
                Console.WriteLine("ReadPostalCodesCsv: {0}", infile);

                var config = new CsvConfiguration(CultureInfo.InvariantCulture)
                {
                    HasHeaderRecord = true,
                    HeaderValidated = null,
                    MissingFieldFound = null,
                    IgnoreBlankLines = true
                };

                using (var reader = new StreamReader(infile))
                using (var csv = new CsvReader(reader, config))
                {
                    csv.Context.RegisterClassMap<PostalCodeMap>();
                    var records = csv.GetRecords<PostalCode>();

                    IEnumerable<PostalCode> rows = csv.GetRecords<PostalCode>();
                    foreach (var obj in rows)
                    {
                        obj.postParse();
                        postalCodes.Add(obj);
                    }
                }
            }
            catch (Exception e)
            {
                Exception baseException = e.GetBaseException();
                Console.WriteLine("Error in ReadPostalCodesCsv: {0}, Message: {1}", e.Message, baseException.Message);
            }
            return postalCodes;
        }

        private static string CurrentDirectory()
        {
            return Directory.GetCurrentDirectory();
        }

        private static char PathSeparator()
        {
            return Path.DirectorySeparatorChar;
        }

        private static string AbsolutePath(string relativeFilename)
        {
            return CurrentDirectory() + PathSeparator() + relativeFilename;
        }

        private static long EpochMsTime()
        {
            return new DateTimeOffset(DateTime.UtcNow).ToUnixTimeMilliseconds();
        }
    }
}
