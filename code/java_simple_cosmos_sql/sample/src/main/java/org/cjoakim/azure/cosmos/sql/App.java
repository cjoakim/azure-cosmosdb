package org.cjoakim.azure.cosmos.sql;

import com.azure.cosmos.ConsistencyLevel;
import com.azure.cosmos.CosmosClient;
import com.azure.cosmos.CosmosClientBuilder;
import com.azure.cosmos.CosmosContainer;
import com.azure.cosmos.CosmosDatabase;
import com.azure.cosmos.CosmosException;

import com.azure.cosmos.models.CosmosContainerProperties;
import com.azure.cosmos.models.CosmosContainerResponse;
import com.azure.cosmos.models.CosmosDatabaseResponse;
import com.azure.cosmos.models.CosmosItemRequestOptions;
import com.azure.cosmos.models.CosmosItemResponse;
import com.azure.cosmos.models.CosmosQueryRequestOptions;
import com.azure.cosmos.models.PartitionKey;
import com.azure.cosmos.models.ThroughputProperties;

import com.azure.cosmos.util.CosmosPagedIterable;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedHashMap;
// import java.util.List;
// import java.util.stream.Collectors;

/**
 * 
 * Chris Joakim, Microsoft, 2021/02/22
 * 
 * See https://docs.microsoft.com/en-us/azure/cosmos-db/sql-api-java-sdk-samples
 * See https://azuresdkdocs.blob.core.windows.net/$web/java/azure-cosmos/latest/index.html
 */
public class App 
{
    public static final double NANOSECONDS_PER_MILLISECONDS = 1000000;  // 1-million

    private static String cliFunction;
    private static String databaseName;
    private static String containerName;

    private static CosmosClient    client;
    private static CosmosDatabase  database;
    private static CosmosContainer container;

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
                        int count = 1;
                        if (args.length > 5) {
                            count = Integer.parseInt(args[5]);
                        }
                        pointRead(pk, id, count);
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

    private static ArrayList<Object> pointRead(String pk, String id, int count) throws Exception {

        log(String.format("pointRead; pk: %s id: %s", pk, id));
        client = createCosmosClient();
        getDatabase();
        getContainer();
        ArrayList<Object> results = null;

        for (int i = 0; i < count; i++) {
            String sql = String.format("select * from c where c.pk ='%s' and c.id = '%s'", pk, id);
            results = executeQuery(sql);
        }
        return results;
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

        long t1 = System.nanoTime();

        CosmosClient client = new CosmosClientBuilder()
                .endpoint(uri)
                .key(key)
                .preferredRegions(prefRegions)
                .consistencyLevel(ConsistencyLevel.EVENTUAL)
                .contentResponseOnWriteEnabled(true)
                .buildClient();

        long t2 = System.nanoTime();
        log("createCosmosClient milliseconds: " + msDiff(t1, t2));
        return client;
    }

    private static void getDatabase() throws Exception {

        log("getDatabase: " + databaseName);
        long t1 = System.nanoTime();
        CosmosDatabaseResponse databaseResponse = 
            client.createDatabaseIfNotExists(databaseName);
        database = client.getDatabase(databaseResponse.getProperties().getId());
        long t2 = System.nanoTime();
        log("getDatabase milliseconds: " + msDiff(t1, t2));
    }

    private static void getContainer() throws Exception {

        log("getContainer: " + containerName);
        long t1 = System.nanoTime();
        CosmosContainerProperties containerProperties =
            new CosmosContainerProperties(containerName, "/pk");
        ThroughputProperties throughputProperties = 
            ThroughputProperties.createManualThroughput(400);
        CosmosContainerResponse containerResponse = 
            database.createContainerIfNotExists(containerProperties, throughputProperties);
        container = database.getContainer(containerResponse.getProperties().getId());
        long t2 = System.nanoTime();
        log("getContainer milliseconds: " + msDiff(t1, t2));
    }

    private static ArrayList<Object> executeQuery(String sql) {

        log("executeQuery: " + sql);
        ArrayList<Object> resultObjects = new ArrayList<Object>();

        // https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/lang/System.html#nanoTime()
        long t1 = System.nanoTime();  // a nanosecond = one billionth of a second

        CosmosQueryRequestOptions options = new CosmosQueryRequestOptions();
        CosmosPagedIterable<Object> items =
                container.queryItems(sql, null, Object.class);
        long t2 = System.nanoTime();

        Iterator it = items.iterator();
        while (it.hasNext()) {
            resultObjects.add(it.next());
        }
        long t3 = System.nanoTime();

        for (Object obj: resultObjects) {
            logResponseObject(obj);
        }
        System.out.println("query items elapsed milliseconds: " + msDiff(t1, t2));
        System.out.println("iterate items elapsed milliseconds: " + msDiff(t1, t3));
        return resultObjects;
    }
        // Results captured on UVM 2/22:
        //    executeQuery: select * from c where c.pk ='SFO' and c.id = '895014e0-1d52-40f6-8ae2-f9dcb0119961'
        //    key: name -> San Francisco Intl
        //    key: city -> San Francisco
        //    key: country -> United States
        //    key: iata_code -> SFO
        //    key: latitude -> 37.618972
        //    key: longitude -> -122.374889
        //    key: altitude -> 13
        //    key: timezone_num -> -8
        //    key: timezone_code -> America/Los_Angeles
        //    key: location -> {type=Point, coordinates=[-122.374889, 37.618972]}
        //    key: pk -> SFO
        //    key: epoch -> 1.613579310177537E9
        //    key: id -> 895014e0-1d52-40f6-8ae2-f9dcb0119961
        //    key: _rid -> 5IsfAOHCY-RfAAAAAAAAAA==
        //    key: _self -> dbs/5IsfAA==/colls/5IsfAOHCY-Q=/docs/5IsfAOHCY-RfAAAAAAAAAA==/
        //    key: _etag -> "0e002cdc-0000-0100-0000-602d442e0000"
        //    key: _attachments -> attachments/
        //    key: _ts -> 1613579310
        //    query items elapsed milliseconds: 0.0496
        //    iterate items elapsed milliseconds: 17.972255
        //    CosmosClient closed

        // Results captured on UVM 2/22, grepped for millis:
        //    createCosmosClient milliseconds: 3250.045701
        //    getDatabase milliseconds: 678.990411
        //    getContainer milliseconds: 71.742525
        //    query items elapsed milliseconds: 5.265046
        //    iterate items elapsed milliseconds: 373.150048
        //    query items elapsed milliseconds: 0.081
        //    iterate items elapsed milliseconds: 28.181345
        //    query items elapsed milliseconds: 0.329103
        //    iterate items elapsed milliseconds: 20.864682
        //    query items elapsed milliseconds: 0.0451
        //    iterate items elapsed milliseconds: 45.835298
        //    query items elapsed milliseconds: 0.073901
        //    iterate items elapsed milliseconds: 48.22492

    private static void logResponseObject(Object obj) {

        try {
            LinkedHashMap hash = (LinkedHashMap) obj;
            Iterator it = hash.keySet().iterator();
            while (it.hasNext()) {
                Object key = it.next();
                Object val = hash.get(key);
                System.out.println(String.format("key: %s -> %s", key, val));
            }
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void displayCommandLineArgs(String[] args) {

        for (int i = 0; i < args.length; i++) {
            log("arg: " + i + " -> " + args[i]);
        }
    }

    private static synchronized String envVar(String name) {

        return System.getenv().get(name);
    }

    private static synchronized double msDiff(long nano1, long nano2) {

        return (nano2 - nano1) / NANOSECONDS_PER_MILLISECONDS;
    }

    private static void log(String msg) {

        System.out.println(msg);
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
}
