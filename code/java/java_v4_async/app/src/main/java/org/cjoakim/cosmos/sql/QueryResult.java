package org.cjoakim.cosmos.sql;


import com.fasterxml.jackson.annotation.JsonIgnore;
import org.cjoakim.cosmos.AppConstants;

import java.util.ArrayList;
import java.util.Map;

/**
 * Instances of this represent the results of a CosmosDB SQL query, including:
 * - the SQL
 * - the result items
 * - the associated Request Unit (RU) costs of the query
 * - the elapsed time in milliseconds
 *
 * Chris Joakim, Microsoft
 */

public class QueryResult implements AppConstants {

    // Instance variables:
    public String sql;
    public String method;
    public ArrayList<Object> items;
    public double totalRequestUnits;
    public long startTime;
    public long finishTime;


    public QueryResult(String sql) {

        super();
        this.sql = sql;
        this.items = new ArrayList<Object>();
        this.totalRequestUnits = 0.0;
        startTimer();
    }

    public String getSql() {
        return sql;
    }

    public void setSql(String sql) {
        this.sql = sql;
    }

    public String getMethod() {
        return method;
    }
    public void setMethod(String m) {
        this.method = m;
    }

    public ArrayList<Object> getItems() {
        return items;
    }

    public Object getItem(int index) {
        return items.get(index);
    }

    public int getItemCount() {
        return items.size();
    }

    public void addItem(Object item) {
        items.add(item);
    }

    public void setItems(ArrayList<Object> items) {
        this.items = items;
    }

    public double getTotalRequestUnits() {
        return totalRequestUnits;
    }

    public void setTotalRequestUnits(double totalRequestUnits) {
        this.totalRequestUnits = totalRequestUnits;
    }

    public void incrementTotalRequestUnits(double d) {
        this.totalRequestUnits = this.totalRequestUnits + d;
    }

    public void startTimer() {
        this.startTime = System.currentTimeMillis();
    }

    public long stopTimer() {
        this.finishTime = System.currentTimeMillis();
        return getElapsedMs();
    }

    public long getElapsedMs() {
        return finishTime - startTime;
    }

    @JsonIgnore
    public long getCountResult() {
        try {
            Map firstItem = (Map) items.get(0);
            return (long) firstItem.get("count");
        }
        catch (Exception e) {
            return -1;
        }
    }
}
