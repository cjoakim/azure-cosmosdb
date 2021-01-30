using System;
using System.Collections;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

using Microsoft.Azure.Cosmos;

// Program to generate votes in a simulated North Carolina election.
// The votes are inserted into CosmosDB by this program, and observed by 
// a change-feed Azure Function.
// Chris Joakim, Microsoft, 2020/11/14


namespace votes_generator {

    class Program {
        private static NCCounties counties = new NCCounties();
        private static Random     random   = new Random();  

        private static readonly string endpointUrl = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_URI");
        private static readonly string primaryKey  = Environment.GetEnvironmentVariable("AZURE_COSMOSDB_SQLDB_KEY");
        private static readonly string databaseId  = "election";
        private static readonly string containerId = "votes";

        static async Task Main(string[] args) {

            int ballots = Int32.Parse(args[0]);
            int sleepMs = Int32.Parse(args[1]);

            CosmosClient client = new CosmosClient(endpointUrl, primaryKey);
            var db = client.GetDatabase(databaseId);
            var container = db.GetContainer(containerId);

            for (int i = 0; i < ballots; i++) {
                VotesMessage vm = new VotesMessage();
                vm.county    = counties.randomCountyNameByPopulation();
                vm.candidate = randomCandidate();
                vm.votes     = randomVoteCount();
                vm.setPk();
                Console.WriteLine(vm.toJson());
                await container.CreateItemAsync(vm, new PartitionKey(vm.pk));
                await Task.Delay(sleepMs);
            }
            client.Dispose();
        }

        private static string randomCandidate() {

            double r = random.NextDouble();
            if (r < 0.5000) {
                return "Adams";
            }
            else {
                return "Brown";
            }
        }

        private static int randomVoteCount() {

            return random.Next(1, 11); 
        }
    }
}
