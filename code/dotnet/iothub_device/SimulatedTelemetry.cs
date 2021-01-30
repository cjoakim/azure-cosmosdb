using System;

namespace CJoakim.IoT
{
    public class SimulatedTelemetry
    {
        public int    seq { get; }
        public double epoch { get; }
        public string device_type { get; }
        public string device_os { get; }
        public string device_version { get; }
        public int    device_pid { get; }
        public int    line_speed { get; }
        public int    temperature { get; }
        public int    humidity { get; }

        public SimulatedTelemetry(int sequence)
        {
            DateTimeOffset dto = DateTimeOffset.UtcNow;
            Random rnd = new Random();

            seq            = sequence;
            epoch          = dto.ToUnixTimeMilliseconds() / 1000.0;
            device_type    = "dotnet";
            device_os      = System.Runtime.InteropServices.RuntimeInformation.OSDescription;
            device_version = System.Runtime.InteropServices.RuntimeInformation.FrameworkDescription;
            device_pid     = System.Diagnostics.Process.GetCurrentProcess().Id;
            line_speed     = rnd.Next(0, 20000); 
            temperature    = rnd.Next(40, 200); 
            humidity       = rnd.Next(50, 100); 
        }
    }
}
