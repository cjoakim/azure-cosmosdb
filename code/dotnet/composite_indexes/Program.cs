using System;

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

// Chris Joakim, Microsoft, 2021/04/08

namespace CJoakim.Cosmos.BulkLoader
{
    public class Program
    {
        // Constants:
        public const string standardPartitionKeyName = "/pk";

        // Class variables:
        private static string[]     programArgs = null;
        private static string       uri = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_URI");
        private static string       key = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_KEY");
        private static string       dbName = "compidx";
        private static string       collName = "coll2";
        private static CosmosClient client = null;
        private static Database     db = null;
        private static Container    container = null;

        static async Task Main(string[] args)
        {
            programArgs = args;
            Console.WriteLine($"args:     {args}");
            Console.WriteLine($"uri:      {uri}");
            Console.WriteLine($"key:      {key}");
            Console.WriteLine($"dbName:   {dbName}");
            Console.WriteLine($"collName: {collName}");

            CosmosClientOptions options = new CosmosClientOptions {
                AllowBulkExecution = true
            };
            client = new CosmosClient(uri, key, options);
            Console.WriteLine("client {0}", client);

            db = await client.CreateDatabaseIfNotExistsAsync(dbName);
            Console.WriteLine("connected to db: {0}", db.Id);

            container = await db.CreateContainerIfNotExistsAsync(collName, standardPartitionKeyName);
            Console.WriteLine("connected to container: {0}", container.Id);

            List<PostalCode> postalCodes = ReadPostalCodesCsv();
            foreach (var obj in postalCodes)
            {
                Console.WriteLine(obj.ToJson());
            }

            List<Task> tasks = new List<Task>(postalCodes.Count);

            int responseCount = 0;

            foreach (PostalCode item in postalCodes)
            {
                tasks.Add(container.CreateItemAsync(item, new PartitionKey(item.pk))
                    .ContinueWith(itemResponse =>
                    {
                        responseCount++;

                        if (itemResponse.IsCompletedSuccessfully)
                        {
                            Console.WriteLine("successful {0} {1}", responseCount, itemResponse.ToString());
                        }
                        else
                        {
                            Console.WriteLine("exception  {0} {1}", responseCount, itemResponse.Exception);
                        }
                    }));
            }

            Console.WriteLine("Tasks created; awaiting completion...");
            
            await Task.WhenAll(tasks);              // Wait until all are done
            Console.WriteLine("Tasks completed");   // Close the client connection

            client.Dispose();
            Console.WriteLine("client disposed");
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

    }
}
