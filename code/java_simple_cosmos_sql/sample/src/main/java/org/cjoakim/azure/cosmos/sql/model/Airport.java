package org.cjoakim.azure.cosmos.sql.model;

import java.util.Map;
import java.util.UUID;

//import org.cjoakim.azure.cosmos.sql.model.Location;

public class Airport {

	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	// Instance variables:
	public String   id;
	public String   pk;
	public String   name;
	public String   city;
	public String   country;
	public String   iata_code;
	public String   latitude;
	public String   longitude;
	public double   altitude;
	public int      timezone_num;
	public String   dst;
	public String   timezone_code;
	public long     epoch;
	public long     _ts;
	public Location location;

	public Airport() {
		
		super();
		//location = new Location();
	}

}
