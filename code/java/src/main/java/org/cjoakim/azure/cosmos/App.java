package org.cjoakim.azure.cosmos;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Example program to access Azure CosmosDB.
 *
 * Chris Joakim, Microsoft, 2018/11/14
 */
public class App {

    // Class variables:
    private static String[] clArgs = null;
    private static String   runFunction = null;


    public static void main( String[] args ) throws Exception {

        if (args.length > 1) {
            clArgs = args;
            runFunction  = clArgs[0];
            System.out.println("runFunction:  " + runFunction);
        }
        else {
            System.err.println("Invalid command-line args, expected runFunction");
            System.exit(1);
        }

        switch (runFunction) {
            case "xxx":
                break;

            default:
                throw new IllegalArgumentException("Invalid runFunction: " + runFunction);
        }
    }

}
