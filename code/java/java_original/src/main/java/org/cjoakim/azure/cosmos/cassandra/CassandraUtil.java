package org.cjoakim.azure.cosmos.cassandra;


import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.security.KeyStore;

import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManagerFactory;

import org.cjoakim.azure.AppConfig;
import org.cjoakim.azure.EnvVarNames;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.Session;
import com.datastax.driver.core.JdkSSLOptions;
import com.datastax.driver.core.RemoteEndpointAwareJdkSSLOptions;

// org.cjoakim.azure.cosmos.cassandra.CassandraUtil

/**
 * @author Chris Joakim, Microsoft
 * @date   2018/11/20
 * 
 * @see    https://docs.microsoft.com/en-us/azure/cosmos-db/create-cassandra-api-account-java
 * @see    mvn archetype:generate -DgroupId=com.azure.cosmosdb.cassandra -DartifactId=cassandra-demo -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
 * @see    https://github.com/Azure-Samples/azure-cosmos-db-cassandra-java-getting-started
 * ------------
 * @see    https://github.com/Azure-Samples/azure-cosmos-db-cassandra-java-getting-started-v4 (Theo VanKraay)
 * @see    https://docs.datastax.com/en/developer/java-driver/4.9/manual/core/
 * 
 * @see    https://azurecosmosdb.github.io/labs/cassandra/labs/04-change_feed_with_spring_data.html
 * @see    https://docs.microsoft.com/en-us/azure/cosmos-db/cassandra-introduction
 * @see    https://docs.microsoft.com/en-us/azure/cosmos-db/create-cassandra-dotnet
 * @see    https://docs.microsoft.com/en-us/azure/cosmos-db/create-cassandra-python
 * @see    https://www.baeldung.com/cassandra-with-java
 */

public class CassandraUtil implements EnvVarNames {

	// Instance variables:
    private Cluster cluster;
    private Session session;
    
    private File   sslKeyStoreFile = null;
    private String sslKeyStorePassword = "changeit";
    
	public CassandraUtil() throws Exception {

		super();


        try {
    		String uri = AppConfig.envVar("AZURE_COSMOSDB_CASSANDRA_URI"); // contact point
    		String user = AppConfig.envVar("AZURE_COSMOSDB_CASSANDRA_USER");
    		String pass = AppConfig.envVar("AZURE_COSMOSDB_CASSANDRA_PASS");
    		int    port = Integer.parseInt(AppConfig.envVar("AZURE_COSMOSDB_CASSANDRA_PORT"));
    		String javaHome = AppConfig.envVar("JAVA_HOME");
    		String keyStoreFilename = javaHome + "/lib/security/cacerts";
    		// /System/Volumes/Data/Library/Java/JavaVirtualMachines/zulu-11.jdk/Contents/Home/lib/security/cacerts
    		
    		System.err.println("uri:    " + uri);
    		System.err.println("user:   " + user);
    		System.err.println("pass:   " + pass);
    		System.err.println("port:   " + port);
    		System.err.println("javaHome:         " + javaHome);
    		System.err.println("keyStoreFilename: " + keyStoreFilename);
    		

            final KeyStore keyStore = KeyStore.getInstance("JKS");
            System.err.println("keyStore:    " + keyStore);
            
            try (final InputStream is = new FileInputStream(keyStoreFilename)) {
                keyStore.load(is, sslKeyStorePassword.toCharArray());
            }

            final KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory
                    .getDefaultAlgorithm()); 
            kmf.init(keyStore, sslKeyStorePassword.toCharArray());
            System.err.println("kmf:    " + kmf);
            
            final TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory
                    .getDefaultAlgorithm());
            tmf.init(keyStore);
            System.err.println("tmf:    " + tmf);
            
            // Creates a socket factory for HttpsURLConnection using JKS contents.
            final SSLContext sc = SSLContext.getInstance("TLSv1.2");
            sc.init(kmf.getKeyManagers(), tmf.getTrustManagers(), new java.security.SecureRandom());
            System.err.println("sc:    " + sc);
            
            JdkSSLOptions sslOptions = RemoteEndpointAwareJdkSSLOptions.builder()
                    .withSSLContext(sc)
                    .build();
            System.err.println("sslOptions:    " + sslOptions);
            
            cluster = Cluster.builder()
                    .addContactPoint(uri)
                    .withPort(port)
                    .withCredentials(user, pass)
                    .withSSL(sslOptions)
                    .withoutJMXReporting() // java.lang.NoClassDefFoundError: com/codahale/metrics/JmxReporter
                    .build();

            System.err.println("cluster:    " + cluster);
            
            try {
				session = cluster.connect();
			}
            catch (Throwable t) {
				t.printStackTrace();
			}
            System.err.println("session:    " + session);
        }
        catch (Exception ex) {
            ex.printStackTrace();
            throw ex;
        }
	}
	
	public static void main(String[] args) throws Exception {
		
		System.err.println("CassandraUtil#main start...");
		
		try {
			if (args.length > 0) {
				String function = args[0].toLowerCase();
				switch (function) {
				
				case "connect":
					connectExample();
					break;
				case "yyy":
					//yyy();
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
	
	private static void connectExample() throws Exception {
		
		CassandraUtil cu = new CassandraUtil();
		System.err.println("cu.session: " + cu.session);
	}

}
