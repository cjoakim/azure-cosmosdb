using System;
using Newtonsoft.Json;


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
