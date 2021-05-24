package org.cjoakim.azure;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Map;
import org.apache.commons.lang3.StringUtils;

/**
 * This class returns configuration values specified as environment variables.
 *
 * See https://12factor.net
 * See https://12factor.net/config
 *
 * @author Chris Joakim, Microsoft
 * @date   2020/11/10
 */

public class AppConfig implements EnvVarNames {

    public static synchronized Map<String, String> envVars() {

        return System.getenv();
    }

    public static synchronized String envVar(String name) {

        return envVars().get(name);
    }

    public static String getCosmosSqlDbAcct() {

        return System.getenv(AZURE_COSMOSDB_SQLDB_ACCT);
    }

    public static String getCosmosSqlDbKey() {

        return System.getenv(AZURE_COSMOSDB_SQLDB_KEY);
    }

    public static String getCosmosSqlDbUri() {

        return System.getenv(AZURE_COSMOSDB_SQLDB_URI);
    }
    
    public static String getCosmosSqlDbName() {

        return System.getenv(AZURE_COSMOSDB_SQLDB_DBNAME);
    }

    public static String getCosmosSqlDbDefaultCollName() {

        return System.getenv(AZURE_COSMOSDB_SQLDB_COLLNAME);
    }
    
    public static String getOpenWeatherMapKey() {

        return System.getenv(AZURE_OPENWEATHERMAP_KEY);
    }

    public static synchronized String storageConnectionString() {

        String acctName = System.getenv(AZURE_STORAGE_ACCOUNT);
        String acctKey  = System.getenv(AZURE_STORAGE_KEY);
        
        String s = System.getenv(AZURE_STORAGE_CONNECTION_STRING);
        // return String.format("DefaultEndpointsProtocol=https;AccountName=%s;AccountKey=%s", acctName, acctKey);
        return s;
    }

    // org.cjoakim.azure.AppConfig
    
    public static void main( String[] args ) throws Exception {

    	Map<String, String> vars = envVars();
    	ArrayList<String> names = new ArrayList<String>();
    	
    	for (String name : vars.keySet())  {
    		names.add(name); 
    	}
    	Collections.sort(names);
    	for (String name : names) { 
    		if (name.startsWith("AZURE")) {
    			StringBuffer sb = new StringBuffer();
    			sb.append("    public static final String ");
    			sb.append(StringUtils.rightPad(name, 38));
    			sb.append(" = \"");
    			sb.append(name);
    			sb.append("\";");
    			System.out.println(sb.toString());
    		}
       }	
    }
}
