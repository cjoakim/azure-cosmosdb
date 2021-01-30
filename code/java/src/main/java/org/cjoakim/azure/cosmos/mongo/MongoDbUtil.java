package org.cjoakim.azure.cosmos.mongo;

import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.mongodb.Block;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;
import com.mongodb.ServerAddress;

import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.MongoCollection;

import com.mongodb.client.MongoCursor;
import com.mongodb.client.result.DeleteResult;
import com.mongodb.client.result.UpdateResult;

import static com.mongodb.client.model.Filters.*;
import static com.mongodb.client.model.Updates.*;

import org.bson.Document;

import org.cjoakim.azure.AppConfig;
import org.cjoakim.azure.EnvVarNames;

/**
 * This class implements Azure CosmosDB/MongoDB operations.
 *
 * @author Chris Joakim, Microsoft
 * @date   2020/11/12
 *
 * @see    https://github.com/Azure-Samples/azure-cosmos-db-mongodb-java-getting-started
 * @see    https://github.com/mongodb/mongo-java-driver
 * @see    https://mongodb.github.io/mongo-java-driver/3.4/driver/getting-started/quick-start/
 */

public class MongoDbUtil implements EnvVarNames {

	// Instance variables:
	private MongoClientURI uri    = null;
	private MongoClient    client = null;
	private MongoDatabase  db     = null;
	private MongoCollection<Document> airportsColl = null;

	public MongoDbUtil() {

		super();

		try {
			// squelch the verbose logging
			Logger comMongoLogger = Logger.getLogger("com.mongodb");
			Logger orgMongoLogger = Logger.getLogger("org.mongodb");
			comMongoLogger.setLevel(Level.SEVERE);
			orgMongoLogger.setLevel(Level.SEVERE);
			
			String connString = AppConfig.envVar(AZURE_COSMOSDB_MONGODB_CONN_STRING);
			String dbName     = AppConfig.envVar(AZURE_COSMOSDB_MONGODB_DBNAME);
			//System.out.println("MongoDbUtil constructor; connString: " + connString);

			uri = new MongoClientURI(connString);
			//System.out.println("MongoClientURI: " + uri);

			client = new MongoClient(uri);
			//System.out.println("MongoClient: " + client);

			db = client.getDatabase(dbName);
			System.out.println("MongoDbUtil; using db: " + db.getName());
		
			airportsColl = db.getCollection("airports");
		}
		catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void close() {
	
		if (client != null) {
			client.close();
			System.out.println("MongoDbUtil#close() completed");
		}
	}
	
	public void addAirportsDocument(Map<String,Object> map) {

		Document doc = new Document(map);
		airportsColl.insertOne(doc);
	}
	
	public long airportsCount() {

		return airportsColl.count();
	}
	
	public ArrayList<Document> findAirportByPk(String pk) {

		ArrayList<Document> documents = new  ArrayList<Document>();
		FindIterable<Document> findIterable = airportsColl.find(eq("pk", pk));
    	MongoCursor<Document> cursor = findIterable.iterator();
    	while (cursor.hasNext()) {
    		documents.add(cursor.next());
    	}
    	cursor.close();
    	return documents;
	}
}
