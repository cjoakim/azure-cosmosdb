using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;
using System;
using System.IO;
using System.Threading.Tasks;
using Newtonsoft.Json;

// dotnet run list_containers --containers 
// dotnet run list_container --container bulkloader
// dotnet run stream_blob --container bulkloader --blob imdb/person_vertices.csv

namespace storage_client
{
    class Program
    {
        private static Config config = null;
        private static BlobServiceClient blobServiceClient = null;
        private static BlobContainerClient containerClient = null;
        
        static async Task Main(string[] args)
        {
            config = new Config(args);
            Console.WriteLine("Hello Storage Client!");

            switch (config.GetRunType())
            {
                case Config.CLI_FUNCTION_LIST_CONTAINERS:
                    await ListContainers();
                    break;
                case Config.CLI_FUNCTION_LIST_CONTAINER:
                    await ListContainer();
                    break;
                case Config.CLI_FUNCTION_STREAM_BLOB:
                    await StreamBlob();
                    break;
                default:
                    Console.WriteLine($"Invalid Config: unknown file run type {config.GetRunType()}");
                    break;
            }
        }

        private static async Task ListContainers()
        {
            await ConnectToStorageAccount();
            foreach (BlobContainerItem ci in blobServiceClient.GetBlobContainers())
            {
                if (config.IsVerbose())
                {
                    Console.WriteLine($"container: {ci.Name} properties: {JsonConvert.SerializeObject(ci.Properties)}");
                }
                else
                {
                    Console.WriteLine($"container: {ci.Name}");
                }
            }
        }

        private static async Task ListContainer()
        {
            await ConnectToStorageContainer();
            await foreach (BlobItem blob in containerClient.GetBlobsAsync())
            {
                if (config.IsVerbose())
                {
                    Console.WriteLine($"blob: {blob.Name} {JsonConvert.SerializeObject(blob.Properties)}");
                }
                else
                {
                    Console.WriteLine($"blob: {blob.Name}");
                }
            }
        }
        private static async Task StreamBlob()
        {
            await ConnectToStorageContainer();
            BlobClient blobClient = containerClient.GetBlobClient(config.GetBlobName());
            int lineCount = 0;
            
            var response = await blobClient.DownloadAsync();
            using (var streamReader = new StreamReader(response.Value.Content))
            {
                while (!streamReader.EndOfStream)
                {
                    var line = await streamReader.ReadLineAsync();
                    lineCount++;
                    Console.WriteLine($"{lineCount} -> {line}");
                }
            }
        }
        
        private static async Task ConnectToStorageAccount()
        {
            if (blobServiceClient != null)
            {
                return;  // already initialized
            }
            string connStr = config.GetStorageConnString();
            if (config.IsVerbose())
            {
                Console.WriteLine($"connection string: {connStr}");
            }
            blobServiceClient = new BlobServiceClient(connStr);
            Console.WriteLine($"connected to account: {blobServiceClient.AccountName}");
            await Task.Delay(0);
        }
        
        private static async Task ConnectToStorageContainer()
        {
            await ConnectToStorageAccount();
            
            string cName = config.GetContainerName();
            Console.WriteLine($"container name: {cName}");
            containerClient = blobServiceClient.GetBlobContainerClient(cName);
            Console.WriteLine($"container uri: {containerClient.Uri}");
            
            await Task.Delay(0);
        }
    }
}
