using System;
using Newtonsoft.Json;

// Instances of this class represent a generic and minimal document in CosmosDB.
//
// Chris Joakim, Microsoft, 2020/10/29

namespace CJoakim.Cosmos
{
    public class GenericDocument
    {
        public string id { get; set; }
        public string pk { get; set; }

        public GenericDocument()
        {
        }

        public string ToJson()
        {
            return JsonConvert.SerializeObject(this);
        }
    }
}
