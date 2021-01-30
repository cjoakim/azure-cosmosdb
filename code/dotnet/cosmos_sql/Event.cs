using System;
using Newtonsoft.Json;

// Instances of this class represent an IoT Event document in CosmosDB.
//
// {
//    "seq": 1,
//    "epoch": 1603814771.667,
//    "device_type": "dotnet",
//    "device_os": "Darwin 19.6.0 Darwin Kernel Version 19.6.0: Mon Aug 31 22:12:52 PDT 2020; root:xnu-6153.141.2~1/RELEASE_X86_64",
//    "device_version": ".NET Core 3.1.9",
//    "device_pid": 8234,
//    "line_speed": 10063,
//    "temperature": 85,
//    "humidity": 80,
//    "EventProcessedUtcTime": "2020-10-27T16:06:11.7363295Z",
//    "PartitionId": 1,
//    "EventEnqueuedUtcTime": "2020-10-27T16:06:11.6930000Z",
//    "IoTHub": {
//        "MessageId": "396ef519-d58f-4c33-8d46-89a609619134",
//        "CorrelationId": "396ef519-d58f-4c33-8d46-89a609619134",
//        "ConnectionDeviceId": "cjiothubdevice2",
//        "ConnectionDeviceGenerationId": "637391385793339080",
//        "EnqueuedTime": "2020-10-27T16:06:11.6930000Z",
//        "StreamId": null
//    },
//    "pk": "cjiothubdevice2|396ef519-d58f-4c33-8d46-89a609619134",
//    "id": "8058029d-b3e5-3aaa-17ad-0ee8168d4774",
//    "_rid": "-+0aAIZz-A4EAAAAAAAAAA==",
//    "_self": "dbs/-+0aAA==/colls/-+0aAIZz-A4=/docs/-+0aAIZz-A4EAAAAAAAAAA==/",
//    "_etag": "\"10007d2e-0000-0100-0000-5f9845750000\"",
//    "_attachments": "attachments/",
//    "_ts": 1603814773
// }
//
// Chris Joakim, Microsoft, 2020/10/29

namespace CJoakim.Cosmos
{
    public class Event
    {
        public int    seq { get; set; }
        public double epoch { get; set; }
        public string device_type { get; set; }
        public string device_os { get; set; }
        public string device_version { get; set; }
        public int    device_pid { get; set; }
        public int    line_speed { get; set; }
        public int    temperature { get; set; }
        public int    humidity { get; set; }

        public string EventEnqueuedUtcTime { get; set; }
        public string EventProcessedUtcTime { get; set; }
        public int    PartitionId { get; set; }
        public string pk { get; set; }
        public string id { get; set; }
        public string _rid { get; set; }
        public string _self { get; set; }
        public string _etag { get; set; }
        public long   _ts { get; set; }

        IoTHub iotHub = null;

        public Event()
        {
            this.iotHub = null;
        }

        public string IoTHubMessageId()
        {
            if (this.iotHub != null)
            {
                return this.iotHub.MessageId;
            }
            else
            {
                return null;
            }
        }

        public string ToJson()
        {
            return JsonConvert.SerializeObject(this);
        }
    }
}
