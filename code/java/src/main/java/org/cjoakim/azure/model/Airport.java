package org.cjoakim.azure.model;

import java.util.Map;
import java.util.UUID;

// AirportId,Name,City,Country,IataCode,IcaoCode,Latitude,Longitude,Altitude,TimezoneNum,Dst,TimezoneCode
// 3876,"Charlotte Douglas Intl","Charlotte","United States","CLT","KCLT",35.214,-80.943139,748,-5,"A","America/New_York"

public class Airport {
	
	// Instance variables:
	protected String   id;
	protected String   pk;
	protected String   doctype;
	protected int      airportId;
	protected String   name;
	protected String   city;
	protected String   country;
	protected String   iataCode;
	protected String   icaoCode;
	protected double   latitude;
	protected double   longitude;
	protected double   altitude;
	protected int      timezoneNum;
	protected String   dst;
	protected String   timezoneCode;
	protected Location location;
	
	
	public Airport() {
		
		super();
		doctype  = "airport";
		location = new Location();
	}
	
	public Airport(Map csvRow) throws Exception {
		
		super();
		doctype  = "airport";
		location = new Location();
		
		// AirportId,Name,City,Country,IataCode,IcaoCode,Latitude,Longitude,Altitude
		// TimezoneNum,Dst,TimezoneCode
		name         = (String) csvRow.get("Name");
		city         = (String) csvRow.get("City");
		country      = (String) csvRow.get("Country");
		iataCode     = (String) csvRow.get("IataCode");
		icaoCode     = (String) csvRow.get("IcaoCode");
		latitude     = Double.parseDouble((String) csvRow.get("Latitude"));
		longitude    = Double.parseDouble((String) csvRow.get("Longitude"));
		altitude     = Double.parseDouble((String) csvRow.get("Altitude"));
		timezoneNum  = Integer.parseInt((String) csvRow.get("TimezoneNum"));
		dst          = (String) csvRow.get("Dst");
		timezoneCode = (String) csvRow.get("TimezoneCode");
		
		setLocationLongitude(longitude);
		setLocationLatitude(latitude);
		setCosmosAttributes();
	}
	
	public void setCosmosAttributes() {
		
		pk = iataCode;
		doctype = "airport";
		if (id == null) {
			id = UUID.randomUUID().toString();
		}
	}
	
	public void setLocationLongitude(double lng) {
		
		location.setLongitude(lng);	
	}
	
	
	public void setLocationLatitude(double lat) {
		
		location.setLatitude(lat);
	}
	
	public boolean hasIataCode() {
		
		if (iataCode == null) {
			return false;
		}
		if (iataCode.trim().length() < 3) {
			return false;
		}
		return true;
	}
	
	// Getters and setters below:
	
	public String getId() {
		return id;
	}

	public void setId(String id) {
		this.id = id;
	}

	public String getPk() {
		return pk;
	}

	public void setPk(String pk) {
		this.pk = pk;
	}

	public String getDoctype() {
		return doctype;
	}

	public void setDoctype(String doctype) {
		this.doctype = doctype;
	}

	public int getAirportId() {
		return airportId;
	}

	public void setAirportId(int airportId) {
		this.airportId = airportId;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getCity() {
		return city;
	}

	public void setCity(String city) {
		this.city = city;
	}

	public String getCountry() {
		return country;
	}

	public void setCountry(String country) {
		this.country = country;
	}

	public String getIataCode() {
		return iataCode;
	}

	public void setIataCode(String iataCode) {
		this.iataCode = iataCode;
	}

	public String getIcaoCode() {
		return icaoCode;
	}

	public void setIcaoCode(String icaoCode) {
		this.icaoCode = icaoCode;
	}

	public double getLatitude() {
		return latitude;
	}

	public void setLatitude(double latitude) {
		this.latitude = latitude;
	}

	public double getLongitude() {
		return longitude;
	}

	public void setLongitude(double longitude) {
		this.longitude = longitude;
	}

	public double getAltitude() {
		return altitude;
	}

	public void setAltitude(double altitude) {
		this.altitude = altitude;
	}

	public int getTimezoneNum() {
		return timezoneNum;
	}

	public void setTimezoneNum(int timezoneNum) {
		this.timezoneNum = timezoneNum;
	}

	public String getDst() {
		return dst;
	}

	public void setDst(String dst) {
		this.dst = dst;
	}

	public String getTimezoneCode() {
		return timezoneCode;
	}

	public void setTimezoneCode(String timezoneCode) {
		this.timezoneCode = timezoneCode;
	}

	public Location getLocation() {
		return location;
	}

	public void setLocation(Location location) {
		this.location = location;
	}

}
