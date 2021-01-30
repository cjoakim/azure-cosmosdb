namespace CJoakim.Cosmos
{

    using System;
    using System.Collections.Generic;
    using System.Globalization;
    using System.IO;
    using CsvHelper;
    using CsvHelper.Configuration;
    using Newtonsoft.Json;

    // Class FileUtil implements IO operations for local data files.
    // Chris Joakim, Microsoft, 2020/10/29

    public class FileUtil
    {
        public FileUtil()
        {
            // Default constructor
        }

        public string CurrentDirectory()
        {
            return Directory.GetCurrentDirectory();
        }

        public char PathSeparator()
        {
           return Path.DirectorySeparatorChar; 
        }

        public string AbsolutePath(string relativeFilename)
        {
            return CurrentDirectory() + PathSeparator() + relativeFilename;
        }

        public List<Airport> ReadAirportsCsv()
        {
            List<Airport> airports = new List<Airport>();
            try {
                string infile = AbsolutePath("data/airports/openflights_airports.csv");
                Console.WriteLine("ReadAirportsCsv: {0}", infile);

                using (var reader = new StreamReader(infile))
                using (var csv = new CsvReader(reader, CultureInfo.CurrentCulture))
                {
                    csv.Configuration.HasHeaderRecord = true;
                    csv.Configuration.HeaderValidated = null;
                    csv.Configuration.MissingFieldFound = null;
                    csv.Configuration.IgnoreBlankLines = true;
                    csv.Configuration.IncludePrivateMembers = false;
                    csv.Configuration.IgnoreReferences = true;

                    var records = csv.GetRecords<Airport>();

                    IEnumerable<Airport> rows = csv.GetRecords<Airport>();
                    foreach (var a in rows)
                    {
                        a.postParse();
                        airports.Add(a);
                    }
                }
            }
            catch (Exception e) {
                Exception baseException = e.GetBaseException();
                Console.WriteLine("Error in ReadAirportsCsv: {0}, Message: {1}", e.Message, baseException.Message);
            }
            return airports;
        }
    }
}
