// ------------------------------------------------------------
//  Copyright (c) Microsoft Corporation.  All rights reserved.
// ------------------------------------------------------------

// Chris Joakim, Microsoft, May 2021

namespace account_explorer
{
    using System;
    using Newtonsoft.Json;
    
    public class Config
    {
        // Constants; environment variables:
        public const string AZURE_COSMOSDB_SQLDB_URI   = "AZURE_COSMOSDB_SQLDB_URI";
        public const string AZURE_COSMOSDB_SQLDB_KEY   = "AZURE_COSMOSDB_SQLDB_KEY";

        // Instance variables:
        private string[] cliArgs = { };

        public Config(string[] args)
        {
            cliArgs = args;  // dotnet run xxx yyy -> args:["xxx","yyy"]
        }

        public string[] GetCliArgs()
        {
            return cliArgs;
        }

        public string FirstArg()
        {
            return cliArgs[0];
        }
        
        public string GetCosmosUri()
        {
            return GetEnvVar(AZURE_COSMOSDB_SQLDB_URI);
        }
        
        public string GetCosmosKey()
        {
            return GetEnvVar(AZURE_COSMOSDB_SQLDB_KEY);
        }
        
        public string GetEnvVar(string name, string defaultValue=null)
        {
            string value = Environment.GetEnvironmentVariable(name);
            if (value == null)
            {
                return defaultValue;
            }
            else
            {
                return value;
            }
        }

        public string GetCliKeywordArg(string keyword, string defaultValue=null)
        {
            try
            {
                for (int i = 0; i < cliArgs.Length; i++)
                {
                    if (keyword == cliArgs[i])
                    {
                        return cliArgs[i + 1];
                    }
                }
                return defaultValue;
            }
            catch
            {
                return defaultValue;
            }
        }
    }
}
