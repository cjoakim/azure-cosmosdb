package org.cjoakim.azure.cosmos.gremlin;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

import org.apache.tinkerpop.gremlin.driver.Client;
import org.apache.tinkerpop.gremlin.driver.Cluster;
import org.apache.tinkerpop.gremlin.driver.Result;
import org.apache.tinkerpop.gremlin.driver.ResultSet;
import org.apache.tinkerpop.gremlin.driver.exception.ResponseException;

import org.cjoakim.azure.AppConfig;
import org.cjoakim.azure.EnvVarNames;
import org.cjoakim.azure.data.DataSource;

import com.fasterxml.jackson.databind.ObjectMapper;


/**
 * @author Chris Joakim, Microsoft
 * @date   2018/11/19
 * @see    https://docs.microsoft.com/en-us/azure/cosmos-db/create-graph-java
 * @see    https://docs.microsoft.com/en-us/azure/cosmos-db/graph-introduction
 * @see    https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-support  (java 3.2.0+)
 * @see    https://tinkerpop.apache.org/javadocs/current/full/
 * @see    https://kelvinlawrence.net/book/Gremlin-Graph-Guide.html
 */

public class GremlinUtil implements EnvVarNames {
	
	// Instance variables:
	private Cluster cluster;
	private Client  client;
	
	
	public GremlinUtil(boolean useYamlConfig) {
		
		super();
		
        try {
        	if (useYamlConfig) {
        		String yamlConfigFile = AppConfig.envVar(AZURE_COSMOSDB_GRAPHDB_YAML_CONFIG_FILE);
        		// /Users/cjoakim/github/cj-azure/code/java/config/gremlin-remote.yaml
        		
        		cluster = Cluster.build(new File(yamlConfigFile)).create();
	            System.out.println("cluster: " + cluster.toString());
	        	
	            client = cluster.connect();
	            System.out.println("client: " + client.toString());
	            System.out.println("client closing: " + client.isClosing());
        	}
        	else {
        		// TODO - the above YAML approach works as of 11/18, but this env-var approach isn't yet
	    		String acct = AppConfig.envVar(AZURE_COSMOSDB_GRAPHDB_ACCT);
	    		String key  = AppConfig.envVar(AZURE_COSMOSDB_GRAPHDB_KEY);
	    		String db   = AppConfig.envVar(AZURE_COSMOSDB_GRAPHDB_DBNAME);
	    		String coll = AppConfig.envVar(AZURE_COSMOSDB_GRAPHDB_GRAPH);
	    		String host = acct + ".gremlin.cosmosdb.azure.com";
	    		String user = String.format("/dbs/%s/colls/%s", db, coll);
	    	
	    		System.out.println("GremlinUtil host: " + host);
	    		System.out.println("GremlinUtil user: " + user);
	    		
	    		String serializerClassname = "org.apache.tinkerpop.gremlin.driver.ser.GraphSONMessageSerializerV2d0";
	    		
	    		Cluster.Builder builder = Cluster.build();
	    		builder.addContactPoint(host);
	    		builder.credentials(user, key);
	    		builder.port(443);
	    		builder.enableSsl(true);
	            System.out.println("builder: " + builder.toString());
	            
	    		Cluster cluster = builder.create();
	            System.out.println("cluster: " + cluster.toString());
	        	
	            client = cluster.connect();
	            System.out.println("client: " + client.toString());
	            System.out.println("client closing: " + client.isClosing());
        	}
        } 
        catch (Exception e) {
            System.out.println("Exception in GremlinUtil constructor");
            e.printStackTrace();
            return;
        }
	}
	
	public GremlinStatementResult submitStatement(String statement) {
		
		List<Result> resultList = new ArrayList<Result>();
		
		GremlinStatementResult gsr = new GremlinStatementResult();
		gsr.setStatement(statement);
		
		try {
			if (statement.startsWith("#")) {  // Allow commented-out lines in the input file
				return gsr;
			}
			System.out.println("\n---\nGremlinUtil#submitStatement: " + statement);
			ResultSet results = client.submit(statement);
			
            CompletableFuture<List<Result>> completableFutureResults;
            CompletableFuture<Map<String, Object>> completableFutureStatusAttributes;
            Map<String, Object> statusAttributes = new HashMap<String, Object>();

            try {
                completableFutureResults = results.all();
                completableFutureStatusAttributes = results.statusAttributes();
                resultList = completableFutureResults.get();
                statusAttributes = completableFutureStatusAttributes.get();            
            }
            catch (ExecutionException | InterruptedException e1) {
                e1.printStackTrace();
                //gsr.setException(e1);
            }
            catch (Exception e2) {
            	//gsr.setException(e2);
                ResponseException re = (ResponseException) e2.getCause();
                
                // Response status codes. You can catch the 429 status code response and work on retry logic.
                System.out.println("Status code: " + re.getStatusAttributes().get().get("x-ms-status-code")); 
                System.out.println("Substatus code: " + re.getStatusAttributes().get().get("x-ms-substatus-code")); 
                
                // If error code is 429, this value will inform how many milliseconds you need to wait before retrying.
                System.out.println("Retry after (ms): " + re.getStatusAttributes().get().get("x-ms-retry-after"));

                // Total Request Units (RUs) charged for the operation, upon failure.
                System.out.println("Request charge: " + re.getStatusAttributes().get().get("x-ms-total-request-charge"));
                
                // ActivityId for server-side debugging
                System.out.println("ActivityId: " + re.getStatusAttributes().get().get("x-ms-activity-id"));
                e2.printStackTrace();
            }

            gsr.setResultList(resultList);
            gsr.setStatusCode(statusAttributes.get("x-ms-status-code").toString());
            gsr.setRequestCharge(statusAttributes.get("x-ms-total-request-charge").toString());
            
            // Status code for successful query. Usually HTTP 200.
            //System.out.println("Status: " + statusAttributes.get("x-ms-status-code").toString());
            // Total Request Units (RUs) charged for the operation, after a successful run.
            // System.out.println("Total charge: " + statusAttributes.get("x-ms-total-request-charge").toString());
            return gsr;
		}
		catch (Exception e) {
			e.printStackTrace();
			return gsr;
		}
	}
	
	public void close() {
		
		if (client != null) {
			System.out.println("GremlinUtil#close");
			client.close();
		}
	}

	public static void main(String[] args) throws Exception {
		
		try {
			if (args.length > 0) {
				String function = args[0].toLowerCase();
				switch (function) {
				
				case "bom_load":
					executeGremlinBomLoadCommands();
					break;
				case "bom_query":
					executeGremlinBomQueryCommands();
					break;
				default:
					System.err.println("ERROR; undefined CLI function: " + function);
				}
			}
			else {
				System.err.println("ERROR; no command-line args");
			}
		}
		catch (Exception e) {
			e.printStackTrace();
			System.exit(1);
		}
		finally {
			System.exit(0);
		}
	}
	
	public static void executeGremlinBomLoadCommands() throws Exception {

		System.out.println("GremlinUtil#executeGremlinBomLoadCommands...");
		GremlinUtil gu = new GremlinUtil(true);
		
		List<String> loadStatements = new DataSource().gremlinBomGraphLoadStatements();
		for (int i = 0; i < loadStatements.size(); i++) {
			if (i < 999999) {
				String statement = loadStatements.get(i);
				GremlinStatementResult gsr = gu.submitStatement(statement);
				if (gsr.completed()) {
					System.out.println("GSR, statement:     " + gsr.getStatement());
					System.out.println("GSR, statusCode:    " + gsr.getStatusCode());
					System.out.println("GSR, requestCharge: " + gsr.formattedRequestCharge());
					System.out.println(toJson(gsr.getResultObjectList(), true));
				}
			}
		}
		gu.close();
		System.out.println("GremlinUtil#executeGremlinBomLoadCommands complete");
	}
	
	public static void executeGremlinBomQueryCommands() throws Exception {

		System.out.println("GremlinUtil#executeGremlinBomQueryCommands...");
		GremlinUtil gu = new GremlinUtil(true);
		
		List<String> statements = new DataSource().gremlinBomGraphQueryStatements();
		for (int i = 0; i < statements.size(); i++) {
			if (i < 100) {
				String statement = statements.get(i);
				GremlinStatementResult gsr = gu.submitStatement(statement);
				if (gsr.completed()) {
					System.out.println("GSR, statement:     " + gsr.getStatement());
					System.out.println("GSR, statusCode:    " + gsr.getStatusCode());
					System.out.println("GSR, requestCharge: " + gsr.formattedRequestCharge());
					System.out.println(toJson(gsr.getResultObjectList(), true));
				}
			}
		}
		gu.close();
		System.out.println("GremlinUtil#executeGremlinBomQueryCommands complete");
	}
	
	private static void printResultsList(List<Result> resultList) throws Exception {
		
		if (resultList != null) {
			int resultCount = resultList.size();
			for (int i = 0; i < resultCount; i++) {
	            System.out.println("Result; idx " + i + "/" + resultCount);
	            Result result = resultList.get(i);
	            Object obj = result.getObject();
	            System.out.println(obj.getClass().getName());  // java.util.LinkedHashMap
	            System.out.println(toJson(obj, true));
			}
		}
        for (Result result : resultList) {
            System.out.println("Result: ");

            Object obj = result.getObject();
            System.out.println(obj.getClass().getName());  // java.util.LinkedHashMap
            System.out.println(toJson(obj, true));
        }
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
}
