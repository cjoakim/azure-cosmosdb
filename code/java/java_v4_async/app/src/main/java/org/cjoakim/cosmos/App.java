/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package org.cjoakim.cosmos;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.cjoakim.cosmos.io.FileUtil;
import org.cjoakim.cosmos.sql.CosmosSqlUtil;
import org.cjoakim.cosmos.sql.QueryBuilder;
import org.cjoakim.cosmos.sql.QueryResult;

import java.util.ArrayList;

public class App {

    // Class variables
    private static Logger logger = LogManager.getLogger(App.class);



    public static void main(String[] args) {

        if (args.length < 1) {
            logger.error("No command-line args; terminating...");
        }
        else {
            try {
                AppConfig.setCommandLineArgs(args);
                String function = args[0];
                String dbName = null;
                String containerName = null;
                String queryNames = null;

                switch (function) {

                    case "display_app_config":
                        displayAppConfig();
                        break;

                    case "execute_queries":
                        dbName = args[1];
                        containerName = args[2];
                        queryNames = args[3];
                        executeQueries(dbName, containerName, queryNames);
                        break;
                    default:
                        logger.error("unknown main function: " + function);
                }
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    private static void displayAppConfig() {

        AppConfig.display(true);
    }


    private static void executeQueries(String dbName, String containerName, String queryNames) {

        logger.warn("executeQueries ...");
        ObjectMapper mapper = new ObjectMapper();
        mapper.enable(SerializationFeature.INDENT_OUTPUT);
        CosmosSqlUtil sqlUtil = null;
        ArrayList<Object> results = null;

        try {
            AppConfig.display(true);

            sqlUtil = new CosmosSqlUtil();
            sqlUtil.setCurrentDatabase(dbName);
            sqlUtil.setCurrentContainer(containerName);

            QueryBuilder queryBldr = new QueryBuilder();
            FileUtil fu = new FileUtil();
            String sql = null;
            QueryResult queryResult;

//            log("---");
//            String pk = "xxx";
//            sql = queryBldr.lookupPeopleInPk(pk);
//            queryResult = sqlUtil.executeDocumentQuery(sql);
//            log(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(queryResult));

            log("---");
            sql = queryBldr.countDocumentsQuery();
            queryResult = sqlUtil.executeCountQuery(sql);
            log(mapper.writerWithDefaultPrettyPrinter().writeValueAsString(queryResult));
            log("count: " + queryResult.getCountResult());

            log("---");
            sql = queryBldr.allDocumentsQuery();
            queryResult = sqlUtil.executeCountQuery(sql);
            fu.writeJson(queryResult, "tmp/all_documents_query.json", true, true);
        }
        catch (Throwable t) {
            t.printStackTrace();
        }
        finally {
            if (sqlUtil != null) {
                sqlUtil.close();
            }
        }
    }

    private static void log(String msg) {

        System.out.println(msg);
    }
}