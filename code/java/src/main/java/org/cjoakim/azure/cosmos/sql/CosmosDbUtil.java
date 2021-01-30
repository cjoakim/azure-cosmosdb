package org.cjoakim.azure.cosmos.sql;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

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

import com.fasterxml.jackson.databind.ObjectMapper;


import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.cjoakim.azure.AppConfig;
import org.cjoakim.azure.EnvVarNames;
import org.cjoakim.azure.data.DataSource;
import org.cjoakim.azure.model.Airport;
import org.cjoakim.io.FileUtil;
import org.cjoakim.utils.Tokenizer;

/**
 * @author Chris Joakim, Microsoft
 * org.cjoakim.azure.cosmosdb.CosmosDbUtil
 * @date   2018/11/18
 * @see    https://github.com/Azure-Samples/azure-cosmos-java-sql-api-samples/blob/master/src/main/java/com/azure/cosmos/examples/crudquickstart/async/SampleCRUDQuickstartAsync.java
 */

public class CosmosDbUtil implements EnvVarNames {

    // Class variables
    private static final Logger logger = LoggerFactory.getLogger(CosmosDbUtil.class);

    // Instance variables:
    private CosmosAsyncClient client;
    private CosmosAsyncDatabase database;
    private CosmosAsyncContainer container;
    
    public CosmosDbUtil() {

		String uri = AppConfig.envVar(AZURE_COSMOSDB_SQLDB_URI);
		String key = AppConfig.envVar(AZURE_COSMOSDB_SQLDB_KEY);
		
        client = new CosmosClientBuilder()
                .endpoint(uri)
                .key(key)
                .preferredRegions(getPreferredRegions())
                .consistencyLevel(ConsistencyLevel.SESSION)
                .contentResponseOnWriteEnabled(true)
                .buildAsyncClient();
        
        System.out.println("CosmosDbUtil constructor: " + client);
    }

	public void createDatabaseIfNotExists(String dbname) throws Exception {
		
        System.out.println("createDatabaseIfNotExists: " + dbname);
        
        Mono<CosmosDatabaseResponse> databaseResponseMono = 
        		client.createDatabaseIfNotExists(dbname);
        databaseResponseMono.flatMap(databaseResponse -> {
            database = client.getDatabase(databaseResponse.getProperties().getId());
            logger.info("Checking database {} completed!\n", database.getId());
            return Mono.empty();
        }).block();
    }
	
    private void createContainerIfNotExists(String cname, String pk) throws Exception {
    	
        System.out.println("createContainerIfNotExists: " + cname);

        CosmosContainerProperties containerProperties =
        	new CosmosContainerProperties(cname, pk);
        Mono<CosmosContainerResponse> containerResponseMono =
        	database.createContainerIfNotExists(
        		containerProperties,
        		ThroughputProperties.createManualThroughput(400));
        
        //  Create container with 400 RU/s
        containerResponseMono.flatMap(containerResponse -> {
            container = database.getContainer(containerResponse.getProperties().getId());
            logger.info("Checking container {} completed!\n", container.getId());
            return Mono.empty();
        }).block();
    }
    
    private List<String> getPreferredRegions() {
    	
    	// Collections.singletonList("West US")
    	
    	ArrayList<String> regions = new ArrayList<String>();
    	try {
			String delimValue = AppConfig.envVar(AZURE_COSMOSDB_SQLDB_PREF_REGIONS);
			if ((delimValue != null) && (delimValue.length() > 0)) {
				Tokenizer t = new Tokenizer();
				return t.tokenizeToArrayList(delimValue, ",");
			}
			else {
				String region = AppConfig.envVar(AZURE_COSMOSDB_SQLDB_PREF_REGION);
				if ((region != null) && (region.length() > 0)) {
					regions.add(region);
				}
			}
		}
    	catch (Exception e) {
			e.printStackTrace();
		}
    	return regions;
    }
    
    private static String toJson(Object obj, boolean pretty) throws Exception {
    		
		ObjectMapper mapper = new ObjectMapper();
		
		if (pretty ) {
			return mapper.writerWithDefaultPrettyPrinter().writeValueAsString(obj);
		}
		else {
			return mapper.writeValueAsString(obj);
		}
    }
    
    public static void main(String[] args) throws Exception {
    
    	System.out.println("org.cjoakim.azure.cosmosdb.CosmosDbUtil main...");
    	
//    	CosmosDbUtil cosmos = new CosmosDbUtil();
//    	cosmos.createDatabaseIfNotExists("dev");
//    	cosmos.createContainerIfNotExists("airports", "/pk");
    	
    	DataSource ds = new DataSource();
    	
    	ArrayList<Airport> airports = ds.readOpenFlightsAirportsCsv();
    	for (int i = 0; i < airports.size(); i++) {
    		//System.out.println(toJson(airports.get(i), true));
    	}
    	
    	Flux<Airport> airportsFlux = ds.openFlightsAirportsFlux();
    	//airportsFlux.subscribe(System.out::println);
    	//airportsFlux.subscribe(a -> processAirport(a));

    	airportsFlux.subscribe(
    		airport -> System.out.println(airport),
    		error   -> System.err.println("Error: " + error)
    	);
    	
    	System.out.println("Airports parsed: " + airports.size());
    	System.out.println("CosmosDbUtil#main complete");
		//System.exit(0);
    }
    
    private static void processAirport(Airport a) {
    	
    	try {
			System.out.println(toJson(a, true));
		}
    	catch (Exception e) {
			e.printStackTrace();
		}
    	return;
    }
}
