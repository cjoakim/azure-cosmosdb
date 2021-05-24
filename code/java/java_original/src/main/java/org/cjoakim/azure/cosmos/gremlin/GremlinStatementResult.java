package org.cjoakim.azure.cosmos.gremlin;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

import org.apache.tinkerpop.gremlin.driver.Result;

/**
 * Instances of this class represent the result of a Gremlin query, or operation.
 * This includes the Gremlin statement string, CosmosDB status code and request charge,
 * and the result objects from the operation.
 *
 * @author Chris Joakim, Microsoft
 * @date   2020/11/19
 */

public class GremlinStatementResult {
	
	// Instance variables:
	public String       statement;
	public int          statusCode;
	public double       requestCharge;
	public List<Result> resultList;
	public String       exceptionMessage;
	
	
	public GremlinStatementResult() {
		
		super();
	}
	
	public boolean completed() {
		
		if (statusCode == 0) {
			return false;
		}
		else {
			return true;
		}
	}
	
	public void setStatusCode(String s) {
	
		try {
			this.statusCode = Integer.parseInt(s);
		}
		catch (NumberFormatException e) {
			this.statusCode = -1;
		}
	}
	
	public void setRequestCharge(String s) {

		try {
			this.requestCharge = Double.parseDouble(s);
		}
		catch (NumberFormatException e) {
			this.requestCharge = -1.0;
		}
	}
	
	public String formattedRequestCharge() {
	
		return new DecimalFormat("###,###.###").format(this.requestCharge);
	}
	
	public void setException(Exception e) {
		
		this.exceptionMessage = e.getClass().getName() + " -> " + e.getMessage();
	}
	
	
	public ArrayList<Object> getResultObjectList() {
		
		ArrayList<Object> objects = new ArrayList<Object>();
		
		if (resultList != null) {
			for (Result r : resultList) {
			    objects.add(r.getObject()); 
			}
		}
		return objects;		
	}
	
	// Simple getter and setter methods below:

	public String getStatement() {
		return statement;
	}

	public void setStatement(String statement) {
		this.statement = statement;
	}

	public int getStatusCode() {
		return statusCode;
	}

	public void setStatusCode(int statusCode) {
		this.statusCode = statusCode;
	}

	public double getRequestCharge() {
		return requestCharge;
	}

	public void setRequestCharge(double requestCharge) {
		this.requestCharge = requestCharge;
	}

	public List<Result> getResultList() {
		return resultList;
	}

	public void setResultList(List<Result> resultList) {
		this.resultList = resultList;
	}

	public String getExceptionMessage() {
		return exceptionMessage;
	}

	public void setExceptionMessage(String exceptionMessage) {
		this.exceptionMessage = exceptionMessage;
	}
}
