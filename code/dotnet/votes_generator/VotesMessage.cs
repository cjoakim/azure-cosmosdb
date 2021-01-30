using System;
using Newtonsoft.Json;

// Instances of this class get created in Program.cs and inserted into CosmosDB.
// Chris Joakim, Microsoft, 2020/11/14

namespace votes_generator {

    public class VotesMessage {

        public string id        { get; }
        public string pk        { get; set; }
        public double epoch     { get; }
        public string county    { get; set; }
        public string candidate { get; set; }
        public int    votes     { get; set; }

        public VotesMessage() {

            id = Guid.NewGuid().ToString();
            DateTimeOffset dto = DateTimeOffset.UtcNow;
            epoch = dto.ToUnixTimeMilliseconds() / 1000.0;
        }

        public void setPk() {

            pk = $"{county}-{candidate}";
        }

        public string toJson() {

            return JsonConvert.SerializeObject(this);
        }
    }
}
