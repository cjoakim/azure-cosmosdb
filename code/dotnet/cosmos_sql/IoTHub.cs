using System;
using Newtonsoft.Json;

// Instances of this class represent the IoTHub portion of an IoT Event document
// in CosmosDB.  The IoTHub attributes are added by the IotHub which processed
// the Event.
//
// "IoTHub": {
//    "MessageId": "396ef519-d58f-4c33-8d46-89a609619134",
//    "CorrelationId": "396ef519-d58f-4c33-8d46-89a609619134",
//    "ConnectionDeviceId": "cjiothubdevice2",
//    "ConnectionDeviceGenerationId": "637391385793339080",
//    "EnqueuedTime": "2020-10-27T16:06:11.6930000Z",
//    "StreamId": null
// }
//
// Chris Joakim, Microsoft, 2020/10/29

namespace CJoakim.Cosmos
{
    public class IoTHub
    {
        public string MessageId { get; set; }
        public string CorrelationId { get; set; }
        public string ConnectionDeviceId { get; set; }
        public string ConnectionDeviceGenerationId { get; set; }
        public string EnqueuedTime { get; set; }
        public string StreamId { get; set; }

        public IoTHub()
        {
            // default constructor
        }

        public string ToJson()
        {
            return JsonConvert.SerializeObject(this);
        }
    }
}
