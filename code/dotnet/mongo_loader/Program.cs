using System;
using MongoDB.Driver;

// See https://mongodb.github.io/mongo-csharp-driver/2.12/getting_started/quick_tour/

namespace mongo_loader {
    class Program{
        private static string[] cliArgs = null;
        private static string dbname   = null;
        private static string collname = null;
        private static string infile   = null;
        private static string target   = "none";
        private static MongoClient client = null;

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
                    Console.WriteLine($"target: {target}, client: {client}, classname: {client.GetType().FullName}");
                }
                else {
                    Console.WriteLine($"client is null for target: {target}");
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
                foreach (string arg in cliArgs) {
                    Console.WriteLine($"arg: {arg}");
                    if (arg.Equals("--targetLocal")) {
                        target = "local";
                    }
                    if (arg.Equals("--targetCosmos")) {
                        target = "cosmos";
                    }
                }
                return true;
            }
            else {
                Console.WriteLine("Invalid command-line args, program exiting:");
                Console.WriteLine("  source env.sh ; dotnet run <dbname> <collname> <infile> [--targetLocal|--targetCosmos]");
                Console.WriteLine("  source env.sh ; dotnet run openflights planes data/openflights__routes.json --targetLocal");
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
            // infile
            
            System.IO.StreamReader file =new System.IO.StreamReader(infile);
            string line = null;
            while ((line = file.ReadLine()) != null) {
                string trimmed = line.Trim();
                Console.WriteLine($"line: {trimmed}");
                

            }
        }
    }
}
