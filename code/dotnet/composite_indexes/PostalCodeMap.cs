
using CsvHelper.Configuration;

// Mapping class for use with the CsvHelper library; maps csv header to object names.
// See https://joshclose.github.io/CsvHelper/getting-started/#reading-a-csv-file
//
// Chris Joakim, Microsoft, 2021/04/10

namespace CJoakim.Cosmos.CompIdx
{
    public class PostalCodeMap : ClassMap<PostalCode>
    {
        public PostalCodeMap()
        {
            // rowId,postalCode,countryCode,cityName,stateAbbrv,latitude,longitude
            Map(m => m.rowId).Name("rowId");
            Map(m => m.postalCode).Name("postalCode");
            Map(m => m.countryCode).Name("countryCode");
            Map(m => m.cityName).Name("cityName");
            Map(m => m.stateAbbrv).Name("stateAbbrv");
            Map(m => m.latitude).Name("latitude");
            Map(m => m.longitude).Name("longitude");
        }
    }
}
