// Chris Joakim, Microsoft, September 2021

namespace CosmosBulkLoader {

    using System;
    using Newtonsoft.Json;

    /**
     * This class is the source of all configuration values for this application -  
     * including environment variables and command-line arguments.  It does this 
     * to support either command-line/terminal/shell or Docker container execution.   
     * With Docker, the command-line can be passed in as environment variable 'CLI_ARGS_STRING'.
     */
    public class Config {
        
        // Constants; environment variable names:
        public const string AZURE_COSMOSDB_SQLDB_CONN_STRING  = "AZURE_COSMOSDB_SQLDB_CONN_STRING";
        public const string AZURE_COSMOSDB_SQLDB_KEY          = "AZURE_COSMOSDB_SQLDB_KEY";
        public const string AZURE_COSMOSDB_SQLDB_URI          = "AZURE_COSMOSDB_SQLDB_URI";
        public const string AZURE_COSMOSDB_SQLDB_PREF_REGIONS = "AZURE_COSMOSDB_SQLDB_PREF_REGIONS";
        public const string AZURE_COSMOSDB_BULK_BATCH_SIZE    = "AZURE_COSMOSDB_BULK_BATCH_SIZE";
        
        // Constants; command-line and keywords:
        public const string VERBOSE_FLAG                          = "--verbose";

        // Class variables:
        private static Config singleton;

        // Instance variables:
        private string[] cliArgs = { };

        public static Config Singleton(string[] args) {  // called by Program.cs Main()
            if (singleton == null) {
                singleton = new Config(args);
            }
            return singleton;
        }

        public static Config Singleton() {  // called elsewhere
            return singleton;
        }

        private Config(string[] args) {
            cliArgs = args;  // dotnet run xxx yyy -> args:["xxx","yyy"]
        }

        public bool IsValid() {
            Console.WriteLine("Config#IsValid args: " + JsonConvert.SerializeObject(cliArgs));
            if (cliArgs.Length < 2) {
                Console.WriteLine("ERROR: empty command-line args");
                return false;
            }
            return true;
        }

        public string[] GetCliArgs() {
            return cliArgs;
        }

        public string GetCosmosConnString() {
            return GetEnvVar(AZURE_COSMOSDB_SQLDB_CONN_STRING, null);
        }

        public string GetCosmosUri() {
            return GetEnvVar(AZURE_COSMOSDB_SQLDB_URI, null);
        }

        public string GetCosmosKey() {
            return GetEnvVar(AZURE_COSMOSDB_SQLDB_KEY, null);
        }
        
        public string[] GetCosmosPreferredRegions() {
            string delimList = GetEnvVar(AZURE_COSMOSDB_SQLDB_PREF_REGIONS, null);
            if (delimList == null) {
                return new string[] { };
            }
            else {
                return delimList.Split(',');
            }
        }

        public string GetEnvVar(string name) {
            return Environment.GetEnvironmentVariable(name);
        }
        
        public string GetEnvVar(string name, string defaultValue = null) {
            string value = Environment.GetEnvironmentVariable(name);
            if (value == null) {
                return defaultValue;
            }
            else {
                return value;
            }
        }

        public string GetCliKeywordArg(string keyword, string defaultValue = null) {
            try {
                for (int i = 0; i < cliArgs.Length; i++) {
                    if (keyword == cliArgs[i]) {
                        return cliArgs[i + 1];
                    }
                }
                return defaultValue;
            }
            catch {
                return defaultValue;
            }
        }

        public bool HasCliFlagArg(string flag) {
            for (int i = 0; i < cliArgs.Length; i++) {
                if (cliArgs[i].Equals(flag)) {
                    return true;
                }
            }
            return false;
        }

        public int BulkBatchSize() {
            string val = GetEnvVar(AZURE_COSMOSDB_BULK_BATCH_SIZE);
            int defaultValue = 100;
            if (val == null) {
                return defaultValue;
            }
            else {
                try {
                    return Int32.Parse(val);
                }
                catch {
                    return defaultValue;
                }
            }
        }

        public bool IsVerbose() {
            for (int i = 0; i < cliArgs.Length; i++) {
                if (cliArgs[i] == VERBOSE_FLAG) {
                    return true;
                }
            }
            return false;
        }

        public void Display() {
            Console.WriteLine($"Config, args: {JsonConvert.SerializeObject(GetCliArgs())}");
        }
    }
}
