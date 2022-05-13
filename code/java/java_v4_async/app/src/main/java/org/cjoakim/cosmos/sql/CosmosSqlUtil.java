package org.cjoakim.cosmos.sql;


import com.azure.cosmos.*;
import com.azure.cosmos.models.CosmosItemResponse;
import com.azure.cosmos.models.CosmosQueryRequestOptions;
import com.azure.cosmos.util.CosmosPagedFlux;
import org.cjoakim.cosmos.AppConfig;
import org.cjoakim.cosmos.AppConstants;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicLong;
import java.util.stream.Collectors;

/**
 * Utility class for CosmosDB/SQL API operations.
 *
 * Chris Joakim, Microsoft
 */

public class CosmosSqlUtil implements AppConstants {

    // Constants
    public static final int DEFAULT_PAGE_SIZE = 1000;

    // Class variables
    private static Logger logger = LogManager.getLogger(CosmosSqlUtil.class);

    // Instance variables
    protected String uri;
    protected CosmosAsyncClient client;
    protected CosmosAsyncDatabase currentDatabase;
    protected CosmosAsyncContainer currentContainer;

    public CosmosSqlUtil() {

        super();

        uri = AppConfig.getCosmosSqlUri();
        String key = AppConfig.getCosmosSqlKey();
        ArrayList<String> prefRegions = AppConfig.getCosmosSqlPrefRegions();

        logger.warn("Creating CosmosAsyncClient with URI: " + uri);

        client = new CosmosClientBuilder()
                .endpoint(uri)
                .key(key)
                .preferredRegions(prefRegions)
                .consistencyLevel(ConsistencyLevel.EVENTUAL)
                .contentResponseOnWriteEnabled(true)
                .buildAsyncClient();

        logger.warn("client created");
    }

    public String getUri() {

        return uri;
    }

    public CosmosAsyncClient getClient() {

        return client;
    }

    public CosmosAsyncDatabase getCurrentDatabase() {

        return currentDatabase;
    }

    public String getCurrentDatabaseName() {

        if (currentDatabase == null) {
            return null;
        }
        else {
            return currentDatabase.getId();
        }
    }

    public void setCurrentDatabase(String dbName) {

        currentDatabase = client.getDatabase(dbName);
    }

    public CosmosAsyncContainer getCurrentContainer() {

        return currentContainer;
    }

    public String getCurrentContainerName() {

        if (currentContainer == null) {
            return null;
        }
        else {
            return currentContainer.getId();
        }
    }

    public void setCurrentContainer(String containerName) {

        currentContainer  = currentDatabase.getContainer(containerName);
    }

//    public void upsertGenericNode(GenericNode node) {
//
//        Mono.just(node).flatMap(item -> {
//            CosmosItemResponse<GenericNode> respItem =
//                    this.currentContainer.upsertItem(node).block();
//            return Mono.empty();
//        }).subscribe();
//    }

    public QueryResult executeDocumentQuery(String sql) {

        logger.warn("executeDocumentQuery, sql: " + sql);
        QueryResult qr = new QueryResult(sql);
        qr.setMethod("executeDocumentQuery");

        CosmosQueryRequestOptions queryOptions = new CosmosQueryRequestOptions();
        CosmosPagedFlux<Map> flux = getCurrentContainer().queryItems(sql, queryOptions, Map.class);

        flux.byPage(DEFAULT_PAGE_SIZE).flatMap(fluxResponse -> {
            List<Map> results = fluxResponse.getResults().stream().collect(Collectors.toList());
            qr.incrementTotalRequestUnits(fluxResponse.getRequestCharge());
            for (int r = 0; r < results.size(); r++) {
                qr.addItem(results.get(r));
            }
            CosmosDiagnostics cd = fluxResponse.getCosmosDiagnostics();
            logger.error("cd: " + cd.toString());
            return Flux.empty();
        }).blockLast();

        qr.stopTimer();
        return qr;
    }

    public QueryResult executeCountQuery(String sql) {

        logger.warn("executeCountQuery, sql: " + sql);
        QueryResult qr = new QueryResult(sql);
        qr.setMethod("executeCountQuery");

        CosmosQueryRequestOptions queryOptions = new CosmosQueryRequestOptions();
        CosmosPagedFlux<Map> flux = getCurrentContainer().queryItems(sql, queryOptions, Map.class);

        flux.byPage(DEFAULT_PAGE_SIZE).flatMap(fluxResponse -> {
            List<Map> results = fluxResponse.getResults().stream().collect(Collectors.toList());
            qr.incrementTotalRequestUnits(fluxResponse.getRequestCharge());
            for (int r = 0; r < results.size(); r++) {
                qr.addItem(results.get(r));
            }
            return Flux.empty();
        }).blockLast();

        qr.stopTimer();
        return qr;
    }

    /**
     * TODO, cj - revisit this, does this method belong here?
     */
    public ArrayList<Object> telemetryInTimeframe(
            String dbName, String cName, long beginTs, long endTs) {

        logger.warn("telemetryInTimeframe in db: " + dbName + ", container: " + cName);
        setCurrentDatabase(dbName);
        setCurrentContainer(cName);

        ArrayList<Object> docs = new ArrayList<Object>();
        int pageSize = 100; // number of docs per page

        StringBuffer sb = new StringBuffer();
        sb.append("select * from c where c._ts >= " + beginTs);
        sb.append(" and c._ts <= " + endTs);
        String sql = sb.toString();
        logger.warn("sql: " + sql);

        CosmosQueryRequestOptions queryOptions = new CosmosQueryRequestOptions();
        CosmosPagedFlux<Map> flux = getCurrentContainer().queryItems(sql, queryOptions, Map.class);

        flux.byPage(pageSize).flatMap(fluxResponse -> {
            List<Map> results = fluxResponse.getResults().stream().collect(Collectors.toList());
            for (int r = 0; r < results.size(); r++) {
                docs.add(results.get(r));
            }
            return Flux.empty();
        }).blockLast();
        return docs;
    }

    public void close() {

        if (client != null) {
            logger.warn("closing client...");
            client.close();
            logger.warn("client closed");
        }
    }
}

