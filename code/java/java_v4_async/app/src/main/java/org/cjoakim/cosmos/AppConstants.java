package org.cjoakim.cosmos;

public interface AppConstants {

    // Environment Variable Names:
    public String AZURE_COSMOSDB_SQLDB_URI            = "AZURE_COSMOSDB_SQLDB_URI";
    public String AZURE_COSMOSDB_SQLDB_KEY            = "AZURE_COSMOSDB_SQLDB_KEY";
    public String AZURE_COSMOSDB_SQLDB_PREF_REGIONS   = "AZURE_COSMOSDB_SQLDB_PREF_REGIONS";

    // Units of Storage
    public final double KB = 1024;
    public final double MB = KB * KB;  // 1,048,576
    public final double GB = KB * KB * KB;
    public final double TB = KB * KB * KB * KB;
}
