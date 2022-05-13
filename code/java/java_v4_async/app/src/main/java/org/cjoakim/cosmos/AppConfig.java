package org.cjoakim.cosmos;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

/**
 * This class is the central point in the application for all configuration values,
 * such as environment variables, command-line arguments, and computed filesystem
 * locations.
 *
 * Chris Joakim, Microsoft
 */

public class AppConfig implements AppConstants {

    // Class variables
    private static Logger logger = LogManager.getLogger(AppConfig.class);
    private static String[] commandLineArgs = new String[0];


    public static void display(boolean extended) {

        logger.warn("AppConfig commandLineArgs.length: " + commandLineArgs.length);
        for (int i = 0; i < commandLineArgs.length; i++) {
            logger.warn("  arg " + i + " -> " + commandLineArgs[i]);
        }
        if (extended) {
            try {
                logger.warn("getCosmosSqlUri:                " + getCosmosSqlUri());
                logger.warn("getCosmosSqlKey:                " + getCosmosSqlKey());
                logger.warn("getCosmosSqlPrefRegions:        " + getCosmosSqlPrefRegions());
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public static void setCommandLineArgs(String[] args) {

        if (args != null) {
            commandLineArgs = args;
        }
    }

    public static boolean booleanArg(String flagArg) {

        for (int i = 0; i < commandLineArgs.length; i++) {
            if (commandLineArgs[i].equalsIgnoreCase(flagArg)) {
                return true;
            }
        }
        return false;
    }

    public static String flagArg(String flagArg) {

        for (int i = 0; i < commandLineArgs.length; i++) {
            if (commandLineArgs[i].equalsIgnoreCase(flagArg)) {
                return commandLineArgs[i + 1];
            }
        }
        return null;
    }

    public static long longFlagArg(String flagArg, long defaultValue) {

        try {
            return Long.parseLong(flagArg(flagArg));
        }
        catch (NumberFormatException e) {
            return defaultValue;
        }
    }

    public static boolean isVerbose() {

        return booleanArg("--verbose");
    }

    public static String getEnvVar(String name) {

        return System.getenv(name);
    }

    public static String getCosmosSqlUri() {

        return System.getenv(AZURE_COSMOSDB_SQLDB_URI);
    }

    public static String getCosmosSqlKey() {

        return System.getenv(AZURE_COSMOSDB_SQLDB_KEY);
    }

    public static ArrayList<String> getCosmosSqlPrefRegions() {

        ArrayList<String> prefRegions = new ArrayList<String>();
        try {
            String[] tokens = System.getenv(AZURE_COSMOSDB_SQLDB_PREF_REGIONS).split(",");
            for (int i = 0; i < tokens.length; i++) {
                prefRegions.add(tokens[i]);
            }
        }
        catch (Exception e) {
            logger.error("Error in getCosmosSqlPrefRegions()");
            e.printStackTrace();
        }
        return prefRegions;
    }
}

