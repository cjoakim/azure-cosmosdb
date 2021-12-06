# 4.01 - Design Process


## Query Driven

- **Focus on the queries** you'll make to your documents, and **not the shape** of the documents
- Be aware of the **RU costs for each operation**; the SDKs and Azure Portal provides this

## Iterative Design, Spreadsheet

The simple and recommended best practice is to:

- Use an Iterative Development approach:
  - Start with a reasonable design
  - Refactor, improve the design with each iteration
  - Repeat as necessary until the results are acceptable/excellent
  - You will learn with each iteration
  - You probably won't get the design right on the first iteration
  - It's schemaless/malleable

- Use of the **CQRS Design Pattern** is recommended
  - Command and Query Responsibility Segregation (CQRS)
  - https://docs.microsoft.com/en-us/azure/architecture/patterns/cqrs
  - An Excel Spreadsheet can be very useful (shown below)

&nbsp;

<p align="center"><img src="img/use-cases-in-excel-v2.png" width="99%"></p>

&nbsp;

- For each Iteration: 
  - First **Identify your use-cases**; what is the list of your database operations?
    - If you're implementing a REST API, what are the endpoints and response documents
      (i.e. - **Swagger/Open API** API definitions)
  - Identify the data that needs to be returned/inserted/upserted for each use-case
  - Identify the SQL for each use case 
  - Identify the **partition key** used, if any, for each of these
  - Strive to use a partition key in most of your queries
  - Optimize the queries with **indexing** (discussed later)
  - **Shape your Documents and Containers to fit the use-cases, not vice-versa**
  - Create a Spreadsheet (i.e. - **Excel**) with this information
  - Add a column for the Estimated Number of Operations per Day
  - Add a column for the RU charge; populate this value as you observe your prototype RU costs 
  - Add a calculated column: Operation Count * RU cost
  - Sum this column; strive for the lowest sum RU total
  - Identify your most expensive operations; refactor/improve in the next iteration

---

## Please don't design your CosmosDB like this

It's not relational.

<p align="center"><img src="img/AdventureWorksLT-ERD.png" width="50%"></p>

---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](0_table_of_contents.md) &nbsp; | &nbsp; [next](4_02_design_considerations.md) &nbsp;
