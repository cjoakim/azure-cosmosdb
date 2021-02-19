package org.cjoakim.azure.cosmos.sql.model;

public class Location {

	// Instance variables:
	protected String type = "Point";
	protected double[] coordinates = {0.0, 0.0};

	public Location() {
		
		super();
	}

	public String getType() {
		
		return type;
	}

	public void setType(String type) {
		
		this.type = type;
	}

	public double[] getCoordinates() {
		
		return coordinates;
	}

	public void setCoordinates(double[] coordinates) {
		
		this.coordinates = coordinates;
	}

	public void setLongitude(double lng) {
		
		this.coordinates[0] = lng;		
	}

	public void setLatitude(double lat) {
		
		this.coordinates[1] = lat;	
	}
}
