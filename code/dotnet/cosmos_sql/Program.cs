using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using Microsoft.Azure.Cosmos;
using Microsoft.Azure.Cosmos.Linq;

// Program entry point, invoked from the command-line.
// Chris Joakim, Microsoft, 2021/01/28

namespace CJoakim.Cosmos
{
    class Program  {

        private static string[] programArgs = null;
        private static int      argCount = 0;

        public static async Task Main(string[] args)
        { 

            try {
                programArgs = args;
                argCount = programArgs.Length;

                int argc = args.Length;
                if (argCount > 0)
                {
                    string f = programArgs[0];
                    string dbname = null;
                    string cname = null;
                    string pk = null;
                    string id = null;
                    int maxCount;
                    int limit;
                    double lat;
                    double lng;
                    double meters;
                    double startEpoch;
                    double endEpoch;

                    switch (programArgs[0])
                    {
                        case "upsertAirports":
                            maxCount = Int32.Parse(programArgs[1]);
                            await upsertAirports(maxCount);
                            break;

                        case "queryAirportsByPk":
                            pk = programArgs[1].ToUpper();
                            await queryAirportsByPk(pk);
                            break;

                        case "queryAirportsByPkId":
                            pk = programArgs[1].ToUpper();
                            id = programArgs[2];
                            await queryAirportsByPkId(pk, id);
                            break;

                        case "queryAirportsByGPS":
                            lng = Double.Parse(programArgs[1]);
                            lat = Double.Parse(programArgs[2]);
                            meters = Double.Parse(programArgs[3]);
                            await queryAirportsByGPS(lng, lat, meters);
                            break;

                        case "queryAirportsByTimezoneOffset":
                            string offset = programArgs[1];
                            await queryAirportsByTimezoneOffset(offset);
                            break;

                        case "queryAirportsPaginated":
                            await queryAirportsPaginated();
                            break;

                        case "queryEvents":
                            startEpoch = Double.Parse(programArgs[1]);
                            endEpoch = Double.Parse(programArgs[2]);
                            await queryEvents(startEpoch, endEpoch);
                            break;

                        case "queryLatestEvents":
                            limit = Int32.Parse(programArgs[1]);
                            await queryLatestEvents(limit);
                            break;

                        case "deleteDocuments":
                            dbname = programArgs[1];
                            cname = programArgs[2];
                            maxCount = Int32.Parse(programArgs[3]);
                            await deleteDocuments(dbname, cname, maxCount);
                            break;

                        case "displayRegions":
                            Console.WriteLine("Displayng the values of a few Regions...");
                            Console.WriteLine($"Regions.EastUS:   {Regions.EastUS}");
                            Console.WriteLine($"Regions.EastUS2:  {Regions.EastUS2}");
                            Console.WriteLine($"Regions.WestUS:   {Regions.WestUS}");
                            Console.WriteLine($"Regions.WestUS2:  {Regions.WestUS2}");
                            Console.WriteLine($"Regions.EastAsia: {Regions.EastAsia}");
                            string regionsEnv = Environment.GetEnvironmentVariable("AZURE_IOT_COSMOSDB_SQLDB_PREF_REGIONS");
                            Console.WriteLine($"Your env var regions: {regionsEnv}");
                            break;

                        default:
                            log("undefined command-line function: " + programArgs[0]);
                            displayUsage();
                            break;
                    }
                }
                else
                {
                    displayUsage();
                }
            }
            catch (Exception e) {
                Console.WriteLine(e);
                Console.WriteLine(e.Message);
            }
            await Task.Delay(10);
        }

        static async Task upsertAirports(int maxCount)
        {
            log($"upsertAirports: {maxCount}");

            FileUtil fsu = new FileUtil();
            List<Airport> airports = new FileUtil().ReadAirportsCsv();
            log($"airports read from csv file: {airports.Count}");

            CosmosUtil cu = new CosmosUtil();
            string dbname = dbNameEnvVar();
            string cname  = "airports";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);

            for (int i = 0; i < airports.Count; i++)
            {
                if (i < maxCount) {
                    Airport a = airports[i];
                    Console.WriteLine(a.ToJson());
                    ItemResponse<Airport> response = await cu.upsertAirportDocument(a);
                    log($"status code:    {response.StatusCode}");
                    log($"request charge: {response.RequestCharge}");
                    log($"diagnostics:    {response.Diagnostics}");
                    log($"resource:       {response.Resource}");
                }
            }
            return;
        }

        static async Task queryEvents(double startEpoch, double endEpoch)
        {
            log($"queryEvents: {startEpoch} to {endEpoch}");

            CosmosUtil cu = new CosmosUtil();
            string dbname = dbNameEnvVar();
            string cname  = "events";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);
            string sql = $"select * from c where c.epoch >= {startEpoch} and c.epoch < {endEpoch}";

            List<dynamic> items = await cu.queryDocuments(sql);

            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
            }
            return;
        }

        static async Task queryLatestEvents(int limit)
        {
            log("queryLatestEvents");

            CosmosUtil cu = new CosmosUtil();
            string dbname = dbNameEnvVar();
            string cname  = "events";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);
            string sql = $"select * from c order by c.epoch desc offset 0 limit {limit}";

            List<dynamic> items = await cu.queryDocuments(sql);

            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
            }
            return;
        }

        static async Task queryAirportsByPk(string pk)
        {
            log("queryAirportsByPk");
            CosmosUtil cu = new CosmosUtil();
            string dbname = dbNameEnvVar();
            string cname  = "airports";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);
            string sql = $"select * from c where c.pk = '{pk}'";

            List<dynamic> items = await cu.queryDocuments(sql);

            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
            }
            return;
        }

        static async Task queryAirportsByTimezoneOffset(string tzOffset)
        {
            // SELECT * FROM c where c.timezone_num = "-5"
            // SELECT c.pk FROM c where c.timezone_num = "-5" offset 1 limit 2
            // SELECT COUNT(1) FROM c     <-- 1459
            // SELECT COUNT(1) FROM c where c.timezone_num = "-5" <-- 522

            // https://docs.microsoft.com/en-us/azure/cosmos-db/sql-query-offset-limit

            log("queryAirportsByTimezoneOffset");
            CosmosUtil cu = new CosmosUtil();
            string dbname = dbNameEnvVar();
            string cname = "airports";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);
            string sql = $"select c.name, c.city, c.longitude, c.timezone_num from c where c.timezone_num = '{tzOffset}'";

            List<dynamic> items = await cu.queryDocuments(sql);

            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
            }
            return;
        }

        static async Task queryAirportsPaginated()
        {
            // SELECT COUNT(1) FROM c  <-- 1459
            // SELECT COUNT(1) FROM c where c.timezone_num = "-5"  <-- 522
            // SELECT c.pk FROM c where c.timezone_num = '-5' order by c.pk offset 140 limit 20

            // https://docs.microsoft.com/en-us/azure/cosmos-db/sql-query-offset-limit
            // https://www.postgresql.org/docs/current/queries-limit.html
            // https://github.com/azure/azure-documentdb-datamigrationtool
            //
            // "The rows skipped by an OFFSET clause still have to be computed inside the server;
            //  therefore a large OFFSET can be inefficient."

            log("queryAirportsPaginated");
            CosmosUtil cu = new CosmosUtil();
            string dbname = dbNameEnvVar();
            string cname = "airports";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);

            string predicate = "where c.timezone_num = '-5'";
            int itemCount = await cu.count(predicate);

            int offset = 0;
            int itemsPerPage = 20;
            log("itemCount:    " + itemCount);
            log("itemsPerPage: " + itemsPerPage);
            double pagesDouble = ((double) itemCount / (double) itemsPerPage);
            double pagesCount = Math.Ceiling(pagesDouble);
            log("pagesCount:   " + pagesCount);

            for (int p = 0; p < pagesCount; p++)
            {
                offset = offset + itemsPerPage;
                string sql = $"SELECT c.pk FROM c {predicate} order by c.pk offset {offset} limit {itemsPerPage}";
                log("===");
                log($"page: {p} sql: {sql}");

                List<dynamic> items = await cu.queryDocuments(sql, itemsPerPage, true);
                for (int i = 0; i < items.Count; i++)
                {
                    Console.WriteLine(items[i]);
                }
            }
            return;
        }


        static async Task queryAirportsByPkId(string pk, string id)
        {
            log("queryAirportsByPkId");
            CosmosUtil cu = new CosmosUtil();
            string dbname = dbNameEnvVar();
            string cname  = "airports";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);
            string sql = $"select * from c where c.pk = '{pk}' and c.id = '{id}'";

            List<dynamic> items = await cu.queryDocuments(sql);

            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
            }
            return;
        }

        static async Task queryAirportsByGPS(double lng, double lat, double meters)
        {
            log("queryAirportsByGPS");
            CosmosUtil cu = new CosmosUtil();
            string dbname = dbNameEnvVar();
            string cname  = "airports";
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);
            string location = $"[{lng}, {lat}]";
            string sql = "select c.pk, c.Name, c.City, c.location.coordinates from c " +
                         "where ST_DISTANCE(c.location, { \"type\": \"Point\", \"coordinates\":" +
                          location + "}) < " + meters;

            List<dynamic> items = await cu.queryDocuments(sql);

            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
            }
            return;
        }

        static async Task deleteDocuments(string dbname, string cname, int maxCount)
        {
            log($"deleteDocuments; db: {dbname}, container: {cname}, maxCount: {maxCount}");

            CosmosUtil cu = new CosmosUtil();
            await cu.setCurrentDatabase(dbname);
            await cu.setCurrentContainer(cname);

            string sql = $"select * from c";
            List<dynamic> items = await cu.queryDocuments(sql, maxCount);

            log($"deleteDocuments, count: {items.Count}");
            for (int i = 0; i < items.Count; i++)
            {
                Console.WriteLine(items[i]);
                log($"deleting item: {items[i].id}, {items[i].pk}");
                string id = items[i].id;
                string pk = items[i].pk;
                GenericDocument doc = new GenericDocument();
                doc.id = items[i].id;
                doc.pk = items[i].pk;

                ItemResponse<GenericDocument> response = await cu.deleteGenericDocument(doc);
                log($"status code:    {response.StatusCode}");
                log($"request charge: {response.RequestCharge}");
            }
        }

        private static string dbNameEnvVar()
        {
            return Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_DBNAME");
        }

        private static void displayUsage()
        {
            log("Usage:");
            log("dotnet run upsertAirports <maxCount>");
            log("dotnet run queryAirportsByPk <pk>");
            log("dotnet run queryAirportsByPk TPA");
            log("dotnet run queryAirportsByPkId TPA c49d4114-f804-4db8-8628-647b45ac9f27");
            log("dotnet run queryAirportsByGPS <latitude> <longitude> <meters>");
            log("dotnet run queryAirportsByGPS -80.848481 35.499254 30000.0 Davidson, NC");
            log("dotnet run queryAirportsByGPS -82.648830 27.867174 10000.0 St. Petersburg, FL");
            log("dotnet run queryAirportsByTimezoneOffset -6");
            log("dotnet run queryAirportsPaginated");
            log("dotnet run queryLatestEvents <limit>");
            log("dotnet run queryLatestEvents 3");
            log("dotnet run queryEvents <startEpoch> <endEpoch>");
            log("dotnet run queryEvents 1604330634 1604330643");
            log("dotnet run deleteDocuments <dbname> <cname> <maxCount>");
            log("dotnet run deleteDocuments dev airports 99999");
            log("dotnet run displayRegions");
        }

        private static void log(String msg)
        {
            Console.WriteLine("" + msg);
        } 
    }
}
