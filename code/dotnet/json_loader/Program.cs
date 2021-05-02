
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

using Microsoft.Azure.Cosmos;

using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

// dotnet run dev sales data/x1.json

namespace json_loader
{
    class Program
    {
        static async Task Main(string[] args)
        {
            if (args.Length > 2)
            {
                string targetDB   = args[0];
                string targetColl = args[1];
                string infile     = args[2];
                // string connStrEnvVar = args[2];
                Console.WriteLine($"args - targetDB: {targetDB}  targetColl: {targetColl}  infile: {infile}");

                JArray documentArray = ReadJsonInfile(infile);
                int counter = 0;

                foreach (JObject doc in documentArray)
                {
                    counter++;
                    // Console.WriteLine($"doc type {doc.GetType().Name}");

                    // Get some values from the JSON document
                    string firstName = doc.GetValue("FirstName").ToString();
                    string lastName  = doc.GetValue("LastName").ToString();
                    string concatName = $"{lastName}, {firstName}";

                    // Add some values to the JSON document
                    doc.Add("Seq", new JValue(counter));
                    doc.Add("ConcatName", new JValue(concatName));


                    // Remove some values from the JSON document
                    doc.Remove("PasswordHash");
                    doc.Remove("PasswordSalt");

                    // Display the document as JSON
                    Console.WriteLine(doc);
                }

            }
            else
            {
                Console.WriteLine("ERROR; invalid command-line args.  See Program.cs Main method.");
            }

            await Task.Delay(0);  // required initially as Main has no async calls

        }

        /**
         * The contents of the given infile are expected to be a JSON Array, not JSON Object.
         * For example, the JSON begins and ends with [] rather than {}.
         */
        private static JArray ReadJsonInfile(string infile)
        {
            string jsonText = System.IO.File.ReadAllText(infile);
            JArray array = JArray.Parse(jsonText);  
            Console.WriteLine($"jsonText read; length: {jsonText.Length}  element count: {array.Count}");
            // jsonText read; length: 463427  element count: 847
            return array;
        }


    }
}
