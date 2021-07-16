using System;
using System.Diagnostics;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using MongoDB.Driver;
using MongoDB.Bson;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

// See https://mongodb.github.io/mongo-csharp-driver/2.12/getting_started/quick_tour/

namespace mongo_loader {
    class Program{
        private static string[] cliArgs = null;
        private static string dbname   = null;
        private static string collname = null;
        private static string infile   = null;
        private static string target   = "none";
        private static bool   verbose  = false;
        private static bool   createNewDocIds = false;
        private static int    lineNumber = 0;
        private static long   tracerInterval = 10000;
        private static int    rowMaxRetries = 20;
        private static long   totalRetryCount = 0;
        private static long   totalFailureCount = 0;
        private static MongoClient client = null;
        private static dynamic databaseObj = null;
        private static dynamic collectionObj = null;
        
        static void Main(string[] args) {
            cliArgs = args;
            if (ReadCommandLineArgs()) {
                Console.WriteLine($"dbname: {dbname} collname: {collname} infile: {infile}");
            }
            else {
                 return;
            }

            try {
                client = CreateMongoClient();
                if (client != null) {
                    Console.WriteLine($"MongoClient create for target: {target}");
                    databaseObj = client.GetDatabase(dbname);  //  MongoDB.Driver.MongoDatabaseImpl
                    collectionObj = databaseObj.GetCollection<BsonDocument>(collname);  // MongoDB.Driver.MongoCollectionImpl
                }
                else {
                    Console.WriteLine($"MongoClient is null for target: {target}");
                }

                ProcessingLoop();
            }
            catch (Exception e) {
                Console.WriteLine(e);
            }
        }

        private static bool ReadCommandLineArgs() {
            Console.WriteLine($"args length: {cliArgs.Length}");
            if (cliArgs.Length > 2) {
                // Positional args
                dbname   = cliArgs[0];
                collname = cliArgs[1];
                infile   = cliArgs[2];
                // Keyword args
                for (int i = 0; i < cliArgs.Length; i++) {
                    string arg = cliArgs[i];
                    Console.WriteLine($"arg: {arg}");
                    if (arg.Equals("--targetLocal")) {
                        target = "local";
                    }
                    if (arg.Equals("--targetCosmos")) {
                        target = "cosmos";
                    }
                    if (arg.Equals("--verbose")) {
                        verbose = true;
                    }
                    if (arg.Equals("--quiet")) {
                        verbose = false;
                    }
                    if (arg.Equals("--createNewDocIds")) {
                        createNewDocIds = true;
                    }
                    if (arg.Equals("--tracerInterval")) {
                        tracerInterval = Int32.Parse(cliArgs[i + 1]);
                    }
                    if (arg.Equals("--rowMaxRetries")) {
                        rowMaxRetries = Int32.Parse(cliArgs[i + 1]);
                    }
                }
                
                Console.WriteLine("Args used this run:"); 
                Console.WriteLine($"  dbname:          {dbname}");
                Console.WriteLine($"  collname:        {collname}");
                Console.WriteLine($"  infile:          {infile}");
                Console.WriteLine($"  target:          {target}");
                Console.WriteLine($"  verbose:         {verbose}");
                Console.WriteLine($"  createNewDocIds: {createNewDocIds}");
                Console.WriteLine($"  tracerInterval:  {tracerInterval}");
                Console.WriteLine($"  rowMaxRetries:   {rowMaxRetries}");
                return true;
            }
            else {
                Console.WriteLine("Invalid command-line args, program exiting:");
                Console.WriteLine("  source env.sh ; dotnet run <dbname> <collname> <infile> [--targetLocal|--targetCosmos] [--verbose|--quiet] --createNewDocIds --tracerInterval x --rowMaxRetries y");
                Console.WriteLine("  source env.sh ; dotnet run openflights planes data/openflights__routes.json --targetLocal --createNewDocIds --tracerInterval 1000 --rowMaxRetries 7");
                return false;
            }
        }

        private static MongoClient CreateMongoClient() {
            if (target.Equals("local")) {
                return CreateLocalMongoClient();
            }
            if (target.Equals("cosmos")) {
                return CreateCosmosMongoClient();
            }
            return null;
        }

        private static MongoClient CreateLocalMongoClient() {
            string user = Environment.GetEnvironmentVariable("M2C_SOURCE_MONGODB_USER");
            string pass = Environment.GetEnvironmentVariable("M2C_SOURCE_MONGODB_PASS");
            string host = Environment.GetEnvironmentVariable("M2C_SOURCE_MONGODB_HOST");
            string port = Environment.GetEnvironmentVariable("M2C_SOURCE_MONGODB_PORT");
            string connStr = $"mongodb://{user}:{pass}@{host}:{port}/admin";
            Console.WriteLine($"connStr: {connStr}");
            return new MongoClient(connStr);
        }
        
        private static MongoClient CreateCosmosMongoClient() {
            string connStr = Environment.GetEnvironmentVariable("M2C_COSMOS_MONGO_CONN_STRING");
            return new MongoClient(connStr);
        }

        private static void ProcessingLoop() {
            long loopStartEpochMs = EpochMsTime();
            LogLineInterval("start", loopStartEpochMs);
            System.IO.StreamReader file = new System.IO.StreamReader(infile);
            string line = null;

            while ((line = file.ReadLine()) != null) {
                long lineStartEpochMs = EpochMsTime();
                lineNumber++;
                for (int i = 0; i < rowMaxRetries; i++) {
                    bool successful = ProcessLine(collectionObj, line.Trim());
                    if (successful) {
                        if (verbose) {
                            long lineElapsedMs = EpochMsTime() - lineStartEpochMs;
                            Console.WriteLine(
                                $"ProcessingLoop - successfully processed line: {lineNumber} : {line} : {i} : {lineElapsedMs}");
                        }
                        break;
                    }
                    totalRetryCount++;
                    Thread.Sleep(1000);
                    if (i == (rowMaxRetries - 1)) {
                        totalFailureCount++;
                    }
                }
                
                if ((lineNumber % tracerInterval) == 0) {
                    LogLineInterval("interval", loopStartEpochMs);
                }
            }
            LogLineInterval("completed", loopStartEpochMs);
            
            // ProcessingLoop - completed, line: 67663, minutes: 1.4711166666666666, retries: 0, failures: 0
        }

        private static void LogLineInterval(string state, long loopStartEpochMs) {
            double elapsedMinutes = ElapsedMsToMinutes(EpochMsTime() - loopStartEpochMs);
            if (state.Equals("start")) {
                elapsedMinutes = 0.0;
            }
            Console.WriteLine(
                $"ProcessingLoop - {state}, line: {lineNumber}, minutes: {elapsedMinutes}, retries: {totalRetryCount}, failures: {totalFailureCount}");
        }

        private static bool ProcessLine(dynamic collectionObj, string line) {

            try {
                JObject jObj = JObject.Parse(line);
                if (createNewDocIds) {
                    jObj.Remove("_id");
                }
                var bsonDoc = jObj.ToBsonDocument();
                if (verbose) {
                    Console.WriteLine($"ProcessLine, bsonDoc: {bsonDoc}");
                }
                collectionObj.InsertOne(bsonDoc);
                return true;
            }
            catch (Exception e) {
                Console.WriteLine($"ProcessLine, error on line: {lineNumber} : {line}");
                Console.WriteLine(e);
                return false;
            }
        }
        
        private static long EpochMsTime() {
            return new DateTimeOffset(DateTime.UtcNow).ToUnixTimeMilliseconds();
        }

        private static double ElapsedMsToMinutes(long elapsedMs) {
            return elapsedMs / 60000.0;
        }
    }
}
