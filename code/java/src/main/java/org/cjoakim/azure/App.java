package org.cjoakim.azure;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.bson.Document;
import org.cjoakim.azure.cosmos.mongo.MongoDbUtil;
import org.cjoakim.azure.cosmos.sql.CosmosDbUtil;
import org.cjoakim.azure.redis.RedisUtil;
import org.cjoakim.azure.storage.BlobUtil;
import org.cjoakim.azure.storage.DataLakeUtil;
import org.cjoakim.io.FileUtil;

import com.mongodb.client.FindIterable;

/**
 * Entry-point for command-line driven program.
 * @author Chris Joakim, Microsoft
 * @date   2020/11/12
 */

public class App implements EnvVarNames {
	
	private static String[] cliArgs = null;
    
    public static void main(String[] args) throws Exception {
    	
    	try {
    		if (args.length > 0) {
    			cliArgs = args;
    			String cliFunction = args[0];
    			
    			switch(cliFunction) {
	    			case "blob":
	    				blobSample();
	    				break;
	    			case "mongoLoadAirports":
	    				String inputFilename = args[1];
	    				mongoLoadAirports(inputFilename);
	    				break;
	    			case "mongoFindAirport":
	    				String pk = args[1];
	    				mongoFindAirport(pk);
	    				break;
	    			case "jedis":
	    				jedisSample();
	    			default:
	    				displayCliOptions("Error; Invalid CLI function: " + cliFunction);
	    				break;
    			}
    		}
    		else {
    			displayCliOptions("Error; No command-line args provided");
    		}
    	}
    	catch (Throwable t) {
    		System.err.println(t.getClass().getName() + "" + t.getMessage());
    	}
    	System.exit(0);
    }
    
    private static void displayCliOptions(String msg) {
    	
    	System.out.println(msg);
    	System.out.println("Class App CLI options:");
    	System.out.println("  blob");
    	System.out.println("  jedis");
    	System.out.println("  mongoLoadAirports <csv-filename>");
    	System.out.println("  mongoFindAirport <iata-pk>");
    }
    
    private static void blobSample() {
    	
    	BlobUtil ru = new BlobUtil();
    	String epoch = "" + System.currentTimeMillis();


    }
    
    private static void mongoLoadAirports(String inputFilename) throws Exception {
    	
    	System.out.println("mongoLoadAirports: " + inputFilename);
    	
    	FileUtil fu = new FileUtil();
    	MongoDbUtil mu = new MongoDbUtil();
    	
    	List<Map> rows = fu.readCsvFile(inputFilename, true, ',');
    	for (int i = 0; i < rows.size(); i++) {
    		Map<String,Object> rowMap = rows.get(i);
    		String iata = (String) rowMap.get("IataCode");
    		if ((iata != null) && (iata.trim().length() > 2)) {
        		rowMap.put("pk", iata.trim());
        		System.out.println(rowMap);
        		mu.addAirportsDocument(rowMap);
    		}
    	}
    	mu.close();
    }
    
    private static void mongoFindAirport(String pk) throws Exception {
    	
    	System.out.println("mongoFindAirport: " + pk);
    	
    	FileUtil fu = new FileUtil();
    	MongoDbUtil mu = new MongoDbUtil();
    	
    	long count = mu.airportsCount();
    	System.out.println("Airport count: " + count);
    	
    	ArrayList<Document> documents = mu.findAirportByPk(pk);
    	for (int i = 0; i < documents.size(); i++) {
    		Document doc = documents.get(i);
    		System.out.println("Airport: " + doc);
    	}
    	mu.close();
    }
    
    private static void jedisSample() {
    	
    	RedisUtil ru = new RedisUtil();
    	String epoch = "" + System.currentTimeMillis();

    	String v1 = ru.get("test");
    	System.out.println("v1: " + v1);
    	
    	ru.set("test", epoch);
    	String v2 = ru.get("test");
    	System.out.println("v2: " + v2);
    	
		//v1: null
		//v2: 1605174280054
    }
}
