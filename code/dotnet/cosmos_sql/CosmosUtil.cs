using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using Microsoft.Azure.Cosmos;
using Newtonsoft.Json;

// This class implements all Azure CosmosDB functionality for this app.
//
// Chris Joakim, Microsoft, 2021/01/28

namespace CJoakim.Cosmos
{
    public class CosmosUtil
    {
        // Constants:
        public const string standardPartitionKeyName = "/pk";

        // Instance variables:
        private CosmosClient client = null;
        private Database     currentDB = null;
        private Container    currentContainer = null;
        private string       continuationToken = null;

        public CosmosUtil()
        {
            string uri = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_URI");
            string key = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_KEY");

            IReadOnlyList<string> prefRegionsList = getPreferredRegions();
            Console.WriteLine("prefRegionsList: " + JsonConvert.SerializeObject(prefRegionsList));

            CosmosClientOptions options = new CosmosClientOptions {
                ApplicationPreferredRegions = prefRegionsList
            };
            this.client = new CosmosClient(uri, key, options);
        }

        private IReadOnlyList<string> getPreferredRegions()
        {
            List<string> regionsList = new List<string>();
            try
            {
                // Example environment variable:
                // AZURE_COSMOSDB_SQLDB_PREF_REGIONS="East US,West US"
                string regionsEnv = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_PREF_REGIONS");
                Console.WriteLine($"regionsEnv: {regionsEnv}");
                
                string[] regionNames = regionsEnv.Split(',');
                for (int i = 0; i < regionNames.Length; i++)
                {
                    switch (regionNames[i])
                    {
                        case Regions.AustraliaCentral:
                            regionsList.Add(Regions.AustraliaCentral);
                            break;
                        case Regions.EastUS:
                            regionsList.Add(Regions.EastUS);
                            break;
                        case Regions.EastUS2:
                            regionsList.Add(Regions.EastUS2);
                            break;
                        case Regions.WestUS:
                            regionsList.Add(Regions.WestUS);
                            break;
                        case Regions.WestUS2:
                            regionsList.Add(Regions.WestUS2);
                            break;
                        case Regions.JapanEast:
                            regionsList.Add(Regions.JapanEast);
                            break;
                        // ... we could add many other Region case statements here ...
                        default:
                            Console.WriteLine($"Unhandled Region: {regionNames[i]}");
                            break;
                    }
                }
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                Console.WriteLine(e.Message);
            }
            return regionsList;
        }

        public async Task setCurrentDatabase(string dbname)
        {
            Console.WriteLine("setting current database to: {0}", dbname);
            this.currentDB = await client.CreateDatabaseIfNotExistsAsync(dbname);
            Console.WriteLine("setCurrentDatabase: {0}", this.currentDB.Id);
        }

        public async Task setCurrentContainer(string cname)
        {
            this.currentContainer =
                await this.currentDB.CreateContainerIfNotExistsAsync(
                    cname, standardPartitionKeyName);
            Console.WriteLine("setCurrentContainer: {0}", this.currentDB.Id);
        }

        public async Task<ItemResponse<Airport>> upsertAirportDocument(Airport airport) {
            string pk = airport.pk + "#1";
            airport.pk = pk;
            ItemResponse<Airport> response =
                await this.currentContainer.UpsertItemAsync<Airport>(
                    airport, new PartitionKey(airport.pk));
            return response;
        }

        public async Task<ItemResponse<Airport>> deleteAirportDocument(Airport airport)
        {
            ItemResponse<Airport> response =
                await this.currentContainer.DeleteItemAsync<Airport>(
                    airport.id, new PartitionKey(airport.pk));
            return response;
        }

        public async Task<ItemResponse<Event>> deleteEventDocument(Event e)
        {
            ItemResponse<Event> response =
                await this.currentContainer.DeleteItemAsync<Event>(
                    e.id, new PartitionKey(e.pk));
            return response;
        }

        public async Task<ItemResponse<GenericDocument>> deleteGenericDocument(GenericDocument doc)
        {
            ItemResponse<GenericDocument> response =
                await this.currentContainer.DeleteItemAsync<GenericDocument>(
                   doc.id, new PartitionKey(doc.pk));
            return response;
        }

        public async Task<List<dynamic>> queryDocuments(string sql, int maxItems=10, bool useContinuation=false)
        {
            Console.WriteLine($"queryDocuments - sql: {sql}");
            double totalRequestCharge = 0;
            List<dynamic> items = new List<dynamic>();

            QueryDefinition queryDefinition = new QueryDefinition(sql);
            QueryRequestOptions requestOptions = new QueryRequestOptions()
            {
                MaxItemCount = maxItems
            };

            FeedIterator<dynamic> queryResultSetIterator = null;

            if (useContinuation)
            {
                queryResultSetIterator =
                     this.currentContainer.GetItemQueryIterator<dynamic>(
                            queryDefinition,
                            continuationToken: this.continuationToken,
                            requestOptions: requestOptions); 
            }
            else
            {
                queryResultSetIterator =
                     this.currentContainer.GetItemQueryIterator<dynamic>(
                            queryDefinition,
                            requestOptions: requestOptions);
            }
            
            while (queryResultSetIterator.HasMoreResults)
            {
                FeedResponse<dynamic> feedResponse =
                    await queryResultSetIterator.ReadNextAsync();
                if (feedResponse.ContinuationToken != null)
                {
                    this.continuationToken = feedResponse.ContinuationToken;
                    Console.WriteLine($"queryDocuments - token: {this.continuationToken}");
                }

                totalRequestCharge += feedResponse.RequestCharge;
                foreach (var item in feedResponse)
                {
                    items.Add(item);
                }
            }
            Console.WriteLine($"queryDocuments - result count: {items.Count}, ru: {totalRequestCharge}");
            return items;
        }

        public async Task<int> count(string predicate)
        {
            int count = -1;
            string sql = ("SELECT COUNT(1) FROM c " + predicate).Trim();
            Console.WriteLine($"count - sql: {sql}");

            QueryDefinition queryDefinition = new QueryDefinition(sql);
            QueryRequestOptions requestOptions = new QueryRequestOptions();
            FeedIterator<dynamic> queryResultSetIterator =
                 this.currentContainer.GetItemQueryIterator<dynamic>(
                        queryDefinition, requestOptions: requestOptions);

            while (queryResultSetIterator.HasMoreResults)
            {
                FeedResponse<dynamic> feedResponse =
                    await queryResultSetIterator.ReadNextAsync();
                foreach (var item in feedResponse)
                {
                    // Item is an instance of Newtonsoft.Json.Linq.JObject
                    string value = item.Property("$1").First.ToString();
                    count = int.Parse(value);
                }
            }
            return count;
        }
    }
}
