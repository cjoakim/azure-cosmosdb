namespace storage_client
{
    using System;
    using Newtonsoft.Json;

    /**
     * This class is the source of all configuration values for this application -  
     * including environment variables and command-line arguments.
     */

    public class Config
    {
        // Constants; environment variables:
        public const string AZURE_STORAGE_CONNECTION_STRING = "AZURE_STORAGE_CONNECTION_STRING";
        public const string AZURE_STORAGE_ACCOUNT           = "AZURE_STORAGE_ACCOUNT";
        public const string AZURE_STORAGE_KEY               = "AZURE_STORAGE_KEY";

        // Constants; command-line and keywords:
        public const string CLI_ARGS_STRING                 = "CLI_ARGS_STRING";  // for executing in a Docker container
        public const string CLI_FUNCTION_LIST_CONTAINERS    = "list_containers";
        public const string CLI_FUNCTION_LIST_CONTAINER     = "list_container";
        public const string CLI_FUNCTION_STREAM             = "stream";
        public const string CONTAINER_KEYWORD               = "--container";
        public const string BLOB_KEYWORD                    = "--blob";
        public const string VERBOSE_FLAG                    = "--verbose";
        
        // Instance variables:
        private string[] cliArgs = { };

        public Config(string[] args)
        {
            cliArgs = args;  // dotnet run xxx yyy -> args:["xxx","yyy"]
            Console.WriteLine($"Config args: {args}");
            
            if (cliArgs.Length == 0)
            {
                // If no args, then the Program was invoked in a Docker container, 
                // so use the CLI_ARGS_STRING environment variable instead.
                cliArgs = GetEnvVar(CLI_ARGS_STRING, "").Split();
                Console.WriteLine("CLI_ARGS: " + JsonConvert.SerializeObject(cliArgs));
            }
        }

        public bool IsValid()
        {
            Console.WriteLine("Config#IsValid args: " + JsonConvert.SerializeObject(cliArgs));

            if (cliArgs.Length < 2)
            {
                Console.WriteLine("ERROR: empty command-line args");
                return false;
            }
            // switch (fileType)
            // {
            //     case FILE_TYPE_VERTEX:
            //         break;
            //     case FILE_TYPE_EDGE:
            //         break;
            //     default:
            //         Console.WriteLine("Invalid Config: unknown file type {0}", fileType);
            //         return false;
            // }

            return true;
        }

        public string[] GetCliArgs()
        {
            return cliArgs;
        }

        public string GetRunType()
        {
            return cliArgs[0].ToLower();
        }
        
        /**
         * This method is intended for unit-testing purposes only; see ConfigTest.cs
         */
        public void SetCliArgs(string commandLine)
        {
            cliArgs = commandLine.Split(" ");
        }

        public string GetStorageConnString()
        {
            return GetEnvVar(AZURE_STORAGE_CONNECTION_STRING, null);
        }

        public string GetEnvVar(string name)
        {
            return Environment.GetEnvironmentVariable(name);
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

        public bool IsVerbose()
        {
            for (int i = 0; i < cliArgs.Length; i++)
            {
                if (cliArgs[i] == VERBOSE_FLAG)
                {
                    return true;
                }
            }
            return false;
        }

        public string GetContainerName()
        {
            return GetCliKeywordArg(CONTAINER_KEYWORD);
        }
        
        public string GetBlobName()
        {
            return GetCliKeywordArg(BLOB_KEYWORD);
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

        public void Display()
        {
            Console.WriteLine("Config:");
            Console.WriteLine($"  args:            {JsonConvert.SerializeObject(GetCliArgs())}");
            Console.WriteLine($"  run type:        {GetRunType()}");
        }
    }
}
