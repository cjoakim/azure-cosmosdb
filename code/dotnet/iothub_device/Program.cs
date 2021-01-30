using System;
using System.Threading;
using System.Threading.Tasks;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.Azure.Devices.Client;

// IoT Hub Client program.
// Generates and sends simulated telemetry JSON messages to the IotHub.
//
// Usage:
//   dotnet run <message-count> <sleep-milliseconds>
//
// Chris Joakim, Microsoft, 2020/11/01

namespace CJoakim.IoT
{
    public class Program
    {
        public static async Task<int> Main(string[] args)
        {
            var messageCount = Int32.Parse(args[0]);
            var sleepMilliseconds = Int32.Parse(args[1]);
            double firstEpoch = 0.0;

            Console.WriteLine("messageCount:      " + messageCount);
            Console.WriteLine("sleepMilliseconds: " + sleepMilliseconds);

            string connString = Environment.GetEnvironmentVariable("AZURE_IOTHUB_DEVICE2_CONN_STR");
            //Console.WriteLine("connString: " + connString);

            using (var deviceClient = DeviceClient.CreateFromConnectionString(connString))
            {
                for (int i = 0; i < messageCount; i++) 
                {
                    var telemetry = new SimulatedTelemetry(1);
                    string messageString = JsonSerializer.Serialize(telemetry);

                    string uuid = Guid.NewGuid().ToString();

                    var message = new Message(Encoding.ASCII.GetBytes(messageString));
                    message.MessageId = uuid;
                    message.CorrelationId = uuid;
                    message.Properties.Add("deviceStartup", (i < 1) ? "true" : "false");

                    await deviceClient.SendEventAsync(message);
                    Console.WriteLine(messageString);
                    await Task.Delay(sleepMilliseconds);

                    if (i == 0)
                    {
                        firstEpoch = telemetry.epoch;
                    }
                }
                Console.WriteLine("messages sent, first epoch timestamp was: " + firstEpoch);
            };
            return 0;
        }
    }
}
