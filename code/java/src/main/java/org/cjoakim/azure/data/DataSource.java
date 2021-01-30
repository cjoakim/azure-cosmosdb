package org.cjoakim.azure.data;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import org.cjoakim.azure.EnvVarNames;
import org.cjoakim.azure.model.Airport;
import org.cjoakim.io.FileUtil;

/**
 * Instances of this class read and return various data, usually from local files.
 * 
 * @author Chris Joakim, Microsoft
 * @date   2018/11/18
 */

public class DataSource  implements EnvVarNames {
	
	public DataSource() {
		
		super();
	}
	
	public ArrayList<Airport> readOpenFlightsAirportsCsv() throws Exception {
		
    	ArrayList<Airport> airports = new ArrayList<Airport>();
    	List<Map> rows = new FileUtil().readCsvFile("data/airports/openflights_airports.csv", true, ',');
    	for (int i = 0; i < rows.size(); i++) {
    		try {
				Airport a = new Airport(rows.get(i));
				if (a.hasIataCode()) {
					airports.add(a);
				}
			}
    		catch (Exception e) {
				System.err.println("error parsing Airport at row index: " + i);
			}
    	}
    	System.out.println("DataSource#readOpenFlightsAirportsCsv; count: " + airports.size());	
    	return airports;
	}
	
	public Flux<Airport> openFlightsAirportsFlux() throws Exception {
		
		return Flux.fromIterable(readOpenFlightsAirportsCsv());
	}
	
	public List<String> gremlinBomGraphLoadStatements() throws Exception {
		
		FileUtil fu = new FileUtil();
		String infile = "data/graph/gremlin_load_file.txt";
		return fu.readFileLines(infile);
	}

	public List<String> gremlinBomGraphQueryStatements() throws Exception {
		
		FileUtil fu = new FileUtil();
		String infile = "data/graph/gremlin_queries.txt";
		return fu.readFileLines(infile);
	}
}
