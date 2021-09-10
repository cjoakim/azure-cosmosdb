// Chris Joakim, Microsoft, September 2021

namespace CosmosBulkLoader {
    
    using System;
    using System.Threading.Tasks;
    using Microsoft.Azure.Cosmos;

    public abstract class CosmosBaseUtil {
        
        protected CosmosClient client = null;
        protected bool         verbose = false;
        protected Database     currentDatabase = null;
        protected Container    currentContainer = null;
        
        protected CosmosBaseUtil() {
            
        }
        
        public async Task<Database> SetCurrentDatabase(string name) {
            try {
                this.currentDatabase = client.GetDatabase(name);
                return await currentDatabase.ReadAsync();
            }
            catch (Exception e) {
                Console.WriteLine($"SetCurrentDatabase {name} -> Exception {e}");
                return null;
            }
        }
        
        public async Task<Container> SetCurrentContainer(string name) {
            try {
                this.currentContainer = this.currentDatabase.GetContainer(name);
                return await currentContainer.ReadContainerAsync();
            }
            catch (Exception e) {
                Console.WriteLine($"SetCurrentContainer {name} -> Exception {e}");
                return null;
            }  
        }
    }
}