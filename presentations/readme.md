



```
globaldb:PRIMARY> use dev
switched to db dev
globaldb:PRIMARY> show collections 
airports
globaldb:PRIMARY> db.airports.findOne()
{
        "_id" : ObjectId("6081be6e24b105653d812998"),
        "name" : "Putnam County Airport",
        "city" : "Greencastle",
        "country" : "United States",
        "iata_code" : "4I7",
        "latitude" : "39.6335556",
        "longitude" : "-86.8138056",
        "altitude" : "842",
        "timezone_num" : "-5",
        "timezone_code" : "America/New_York",
        "location" : {
                "type" : "Point",
                "coordinates" : [
                        -86.8138056,
                        39.6335556
                ]
        }
}
globaldb:PRIMARY> db.runCommand({getLastRequestStatistics: 1})
{
        "CommandName" : "find",
        "RequestCharge" : 5.27,
        "RequestDurationInMilliSeconds" : NumberLong(161),
        "EstimatedDelayFromRateLimitingInMilliseconds" : NumberLong(0),
        "RetriedDueToRateLimiting" : false,
        "ActivityId" : "535bc56d-9e37-4b4e-8086-fc562846e3bd",
        "ok" : 1
}
```
