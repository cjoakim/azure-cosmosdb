using System;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Linq;
using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Spreadsheet;
using Newtonsoft.Json;

// https://www.nuget.org/packages/DocumentFormat.OpenXml/
// https://docs.microsoft.com/en-us/dotnet/api/documentformat.openxml.packaging.spreadsheetdocument?view=openxml-2.8.1

// dotnet run read_excel_file data/adventureworks-customers.xlsx 

namespace excel_to_cosmos
{
    class Program
    {
        private static string[] programArgs = null;
        public static async Task Main(string[] args)
        {
            programArgs = args;
            string function = args[0];

            switch (programArgs[0])
            {
                case "read_excel_file":
                    string filename = args[1];
                    await ReadExcelFile(filename);
                    break;
                default:
                    Console.WriteLine();
                    break;
            }
        }

        private static async Task ReadExcelFile(string filename)
        {
            Console.WriteLine($"ReadExcelFile: {filename}");
            
            using (SpreadsheetDocument spreadsheetDocument = 
                SpreadsheetDocument.Open(filename, false))
            {
                WorkbookPart workbookPart = spreadsheetDocument.WorkbookPart;
                WorksheetPart worksheetPart = workbookPart.WorksheetParts.First();
                SheetData sheetData = worksheetPart.Worksheet.Elements<SheetData>().First();
                int rowNumber = 0;
                int colNumber = 0;
                List<string> headerNames = new List<string>();
                List<Dictionary<string, string>> rowObjects = new List<Dictionary<string, string>>();
                
                foreach (Row r in sheetData.Elements<Row>())
                {
                    rowNumber++;
                    colNumber = 0;
                    Dictionary<string, string> rowDict = new Dictionary<string, string>();

                    foreach (Cell c in r.Elements<Cell>())
                    {
                        string text = "";
                        
                        text = c.InnerText;

                        if (rowNumber == 1)
                        {
                            headerNames.Add(text.Trim());
                        }
                        else
                        {
                            rowDict.Add(headerNames[colNumber], text.Trim());
                        }

                        Console.WriteLine($"{rowNumber} {colNumber} -> {text}");
                        colNumber++;
                    }

                    if (rowNumber > 1)
                    {
                        rowObjects.Add(rowDict);
                    }
                }
                Console.WriteLine("rowObjects\n" + JsonConvert.SerializeObject(rowObjects, Formatting.Indented));
            }
            await Task.Delay(10);
        }
    }
}

// CustomerID	NameStyle	Title	FirstName	MiddleName	LastName	Suffix	CompanyName	SalesPerson	EmailAddress	Phone	PasswordHash	PasswordSalt	rowguid	ModifiedDate