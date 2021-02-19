package org.cjoakim.azure.cosmos.sql;

import com.azure.cosmos.ConsistencyLevel;
import com.azure.cosmos.CosmosClient;
import com.azure.cosmos.CosmosClientBuilder;
import com.azure.cosmos.CosmosContainer;
import com.azure.cosmos.CosmosDatabase;
import com.azure.cosmos.CosmosException;

// import com.azure.cosmos.examples.common.AccountSettings;
// import com.azure.cosmos.examples.common.Families;
// import com.azure.cosmos.examples.common.Family;

import com.azure.cosmos.models.CosmosContainerProperties;
import com.azure.cosmos.models.CosmosContainerResponse;
import com.azure.cosmos.models.CosmosDatabaseResponse;
import com.azure.cosmos.models.CosmosItemRequestOptions;
import com.azure.cosmos.models.CosmosItemResponse;
import com.azure.cosmos.models.CosmosQueryRequestOptions;
import com.azure.cosmos.models.PartitionKey;
import com.azure.cosmos.models.ThroughputProperties;

// import com.azure.cosmos.util.CosmosPagedIterable;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * 
 * Chris Joakim, Microsoft, 2021/02/19
 * 
 * See https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-java-sdk-samples
 *
 */
public class App 
{
    protected static Logger logger = LoggerFactory.getLogger(App.class);
    // http://www.slf4j.org/manual.html
    // http://www.slf4j.org/api/org/slf4j/impl/SimpleLogger.html
    // https://logging.apache.org/log4j/2.x/manual/configuration.html

    private static String cliFunction;
    private static String databaseName;
    private static String containerName;

    private static CosmosClient    client;
    private static CosmosDatabase  database;
    private static CosmosContainer container;


    /**
     * 
     * point_read <db> <container> <pk> <id>
     * query <db> <container> <query-id>
     */
    public static void main(String[] args)
    {
        displayCommandLineArgs(args);

        if (args.length > 3) {
            try {
                cliFunction   = args[0];
                databaseName  = args[1];
                containerName = args[2];

                switch (cliFunction) {
                    case "point_read":
                        String pk = args[3];
                        String id = args[4];
                        pointRead(pk, id);
                        break;
    
                    default:
                        displayCommandLineOptions("Invalid CLI function: " + cliFunction);
                }
            }
            catch (Exception e) {
                log(String.format("Cosmos getStarted failed with %s", e));
                e.printStackTrace();
            }
            finally {
                if (client != null) {
                    try {
                        client.close();
                        log("CosmosClient closed");
                        System.exit(0);
                    }
                    catch (Exception e2) {
                        log("ERROR closing CosmosClient");
                        e2.printStackTrace();
                    }
                }
            }
        }
        else {
            displayCommandLineOptions("Invalid command-line args");
        }
    }

    private static void pointRead(String pk, String id) throws Exception {

        log(String.format("pointRead; pk: %s id: %s", pk, id));
        client = createCosmosClient();
        getDatabase();
        getContainer();

    }

    private static CosmosClient createCosmosClient() {

        // Read configuration values from environment variables:
        String uri    = envVar("AZURE_COSMOSDB_SQLDB_URI");
        String key    = envVar("AZURE_COSMOSDB_SQLDB_KEY");
        String region = envVar("AZURE_COSMOSDB_SQLDB_PREF_REGION");
        log("uri:     " + uri);
        log("key len: " + key.length());
        log("region:  " + region);

        ArrayList<String> prefRegions = new ArrayList<String>();
        prefRegions.add(region);  // we could add more regions here

        long t1 = System.currentTimeMillis();

        CosmosClient client = new CosmosClientBuilder()
                .endpoint(uri)
                .key(key)
                .preferredRegions(prefRegions)
                .consistencyLevel(ConsistencyLevel.EVENTUAL)
                .contentResponseOnWriteEnabled(true)
                .buildClient();

        long t2 = System.currentTimeMillis();
        log("createCosmosClient ms: " + (t2 - t1));
        return client;
    }

    private static void getDatabase() throws Exception {

        log("getDatabase: " + databaseName);
        long t1 = System.currentTimeMillis();
        CosmosDatabaseResponse databaseResponse = 
            client.createDatabaseIfNotExists(databaseName);
        database = client.getDatabase(databaseResponse.getProperties().getId());
        long t2 = System.currentTimeMillis();
        log("getDatabase ms: " + (t2 - t1));
    }

    private static void getContainer() throws Exception {

        log("getContainer: " + containerName);
        long t1 = System.currentTimeMillis();
        CosmosContainerProperties containerProperties =
            new CosmosContainerProperties(containerName, "/pk");
        ThroughputProperties throughputProperties = 
            ThroughputProperties.createManualThroughput(400);
        CosmosContainerResponse containerResponse = 
            database.createContainerIfNotExists(containerProperties, throughputProperties);
        container = database.getContainer(containerResponse.getProperties().getId());
        long t2 = System.currentTimeMillis();
        log("getContainer ms: " + (t2 - t1));
    }

    private static void displayCommandLineArgs(String[] args) {

        for (int i = 0; i < args.length; i++) {
            log("arg: " + i + " -> " + args[i]);
        }
    }

    private static void displayCommandLineOptions(String msg) {

        System.out.println("");
        if (msg != null) {
            System.out.println("ERROR: " + msg);
        }
        System.out.println("Command-line samples; see run.sh");
        System.out.println("  point_read <db> <container> <pk> <id>");
        System.out.println("  point_read dev airports SFO 895014e0-1d52-40f6-8ae2-f9dcb0119961");
        System.out.println("  query <db> <container> <query-id>");
        System.out.println("");
    }

    private static void log(String msg) {

        System.out.println(msg);
    }

    private static synchronized String envVar(String name) {

        return System.getenv().get(name);
    }
}
