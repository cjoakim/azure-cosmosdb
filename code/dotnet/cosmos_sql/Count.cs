using System;
using Newtonsoft.Json;

// Instances of this class represent an Airport in the OpenFlights CSV data, like this:
// AirportId,Name,City,Country,IataCode,IcaoCode,Latitude,Longitude,Altitude,TimezoneNum,Dst,TimezoneCode
// 3682,"Hartsfield Jackson Atlanta Intl","Atlanta","United States","ATL","KATL",33.636719,-84.428067,1026,-5,"A","America/New_York"
//
// Chris Joakim, Microsoft, 2020/10/29

namespace CJoakim.Cosmos
{
    public class Count
    {
        public string n { get; set; }



        public Count()
        {
            // Default constructor
        }

        public string ToJson()
        {
            return JsonConvert.SerializeObject(this);
        }
    }
}
