using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;
using System;
using System.IO;
using System.Threading.Tasks;
using Newtonsoft.Json;

// dotnet run list_container --container imdb 

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
                case Config.CLI_FUNCTION_LIST_CONTAINER:
                    await ListContainer();
                    break;
                case Config.CLI_FUNCTION_STREAM:
                    await StreamBlob();
                    break;
                default:
                    Console.WriteLine($"Invalid Config: unknown file run type {config.GetRunType()}");
                    break;
            }
        }

        private static async Task ListContainer()
        {
            await connectToStorageContainer();
            
            await foreach (BlobItem blob in containerClient.GetBlobsAsync())
            {
                Console.WriteLine($"blob: {blob.Name} {JsonConvert.SerializeObject(blob.Properties)}");
            }
        }
        
        private static async Task StreamBlob()
        {
            await connectToStorageContainer();
        }

        private static async Task ConnectToStorageAccount()
        {
            string connStr = config.GetStorageConnString();
            Console.WriteLine($"connection string: {connStr}");
            blobServiceClient = new BlobServiceClient(connStr);
            Console.WriteLine($"connected to account: {blobServiceClient.AccountName}");
            
            await Task.Delay(0);
        }
        
        private static async Task ListContainers()
        {
            foreach (BlobContainerItem container in blobServiceClient.GetBlobContainers())
            {
                Console.WriteLine($"container: {container.Name}");
            }
            await Task.Delay(0);
        }
        
        private static async Task connectToStorageContainer()
        {
            string connStr = config.GetStorageConnString();
            Console.WriteLine($"connection string: {connStr}");
            blobServiceClient = new BlobServiceClient(connStr);
            Console.WriteLine($"account: {blobServiceClient.AccountName}");
            

            

            string cName = config.GetContainerName();
            Console.WriteLine($"container name: {cName}");
            containerClient = blobServiceClient.GetBlobContainerClient(cName);
            Console.WriteLine($"container uri: {containerClient.Uri}");
            
            await Task.Delay(0);
        }
    }
}
