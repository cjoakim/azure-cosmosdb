package org.cjoakim.cosmos;

import com.azure.cosmos.ConsistencyLevel;
import com.azure.cosmos.CosmosAsyncClient;
import com.azure.cosmos.CosmosAsyncContainer;
import com.azure.cosmos.CosmosAsyncDatabase;
import com.azure.cosmos.CosmosClientBuilder;
import com.azure.cosmos.CosmosException;

import com.azure.cosmos.models.CosmosContainerProperties;
import com.azure.cosmos.models.CosmosContainerRequestOptions;
import com.azure.cosmos.models.CosmosContainerResponse;
import com.azure.cosmos.models.CosmosDatabaseResponse;
import com.azure.cosmos.models.CosmosItemResponse;
import com.azure.cosmos.models.CosmosQueryRequestOptions;
import com.azure.cosmos.models.PartitionKey;
import com.azure.cosmos.models.ThroughputProperties;

import com.azure.cosmos.util.CosmosPagedFlux;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.Duration;
import java.util.ArrayList;
import java.util.stream.Collectors;

/**
 * SELECT DISTINCT VALUE a.pk FROM airports a
 * See https://github.com/Azure-Samples/azure-cosmos-java-sql-api-samples/blob/main/src/main/java/com/azure/cosmos/examples/crudquickstart/async/SampleCRUDQuickstartAsync.java
 * https://docs.microsoft.com/en-us/azure/cosmos-db/create-sql-api-java?tabs=sync#clone-the-sample-application
 */
public class App 
{
    // Constants:
    private static final String databaseName  = "dev";
    private static final String containerName = "airports";

    // Class variables:
    private static CosmosAsyncClient client;
    private static CosmosAsyncDatabase  database;
    private static CosmosAsyncContainer container;
    //protected static Logger logger = LoggerFactory.getLogger(App.class);

    public static void main( String[] args )
    {
        System.out.println( "start of main" );
        try {
            createClient();
            getDatabaseReference();
            getContainerReference();
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        finally {
            close();
        }
        System.out.println( "end of main" );
    }

    private static void createClient() throws Exception {

        String uri    = envVar("AZURE_COSMOSDB_SQLDB_URI");
        String key    = envVar("AZURE_COSMOSDB_SQLDB_KEY");
        String region = "East US"; //envVar("AZURE_COSMOSDB_SQLDB_PREF_REGION");
        ArrayList<String> prefRegions = new ArrayList<String>();
        prefRegions.add(region);

        client = new CosmosClientBuilder()
                .endpoint(uri)
                .key(key)
                .preferredRegions(prefRegions)
                .contentResponseOnWriteEnabled(true)
                .consistencyLevel(ConsistencyLevel.EVENTUAL)
                .buildAsyncClient();

        System.out.println("client created: " + client);
    }

    private static void getDatabaseReference() {

        Mono<CosmosDatabaseResponse> databaseResponseMono =
                client.createDatabaseIfNotExists(databaseName);
        databaseResponseMono.flatMap(databaseResponse -> {
            database = client.getDatabase(databaseResponse.getProperties().getId());
            System.out.println("getDatabaseReference completed: " + database.getId());
            return Mono.empty();
        }).block();
        System.out.println("database: " + database);
    }

    private static void getContainerReference() {

        CosmosContainerProperties containerProperties =
                new CosmosContainerProperties(containerName, "/pk");
        Mono<CosmosContainerResponse> containerResponseMono =
                database.createContainerIfNotExists(
                        containerProperties, ThroughputProperties.createManualThroughput(400));
        containerResponseMono.flatMap(containerResponse -> {
            container = database.getContainer(containerResponse.getProperties().getId());
            System.out.println("getContainerReference completed; " + container.getId());
            return Mono.empty();
        }).block();
        System.out.println("container: " + container);
    }

    private static synchronized String envVar(String name) {

        return System.getenv().get(name);
    }

    private static void close() {

        if (client != null) {
            System.out.println("closing client");
            client.close();
        }
    }
}

