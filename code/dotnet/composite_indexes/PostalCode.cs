using System;
using Newtonsoft.Json;


// Chris Joakim, Microsoft, 2021/04/10

namespace CJoakim.Cosmos.CompIdx

{
    public class PostalCode
    {
        // rowId,postalCode,countryCode,cityName,stateAbbrv,latitude,longitude
        public string id { get; set; }
        public string rowId { get; set; }
        public string pk { get; set; }
        public string postalCode { get; set; }
        public string countryCode { get; set; }
        public string cityName { get; set; }
        public string stateAbbrv { get; set; }
        public double latitude { get; set; }
        public double longitude { get; set; }
        public Location location { get; set; }


        public PostalCode()
        {
            // Default constructor
        }



        public void postParse()
        {
            pk = stateAbbrv;
            this.location = new Location(this.latitude, this.longitude);
            if (this.id == null)
            {
                this.id = Guid.NewGuid().ToString();
            }
        }

        public string ToJson()
        {
            return JsonConvert.SerializeObject(this);
        }
    }
}
