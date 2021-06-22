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

- For each Iteration: 
  - First **Identify your use-cases**; what is the list of your database operations?
    - If you're implementing a REST API, what are the endpoints and response documents (i.e. - Swagger API definitions)
  - Identify the data that needs to be returned/inserted/upserted for each use-case
  - Identify the SQL for each use case 
  - Identify the partition key used, if any, for each of these
  - Strive to use a partition key in most of your queries
  - Optimize the queries with Indexing (discussed later)
  - **Shape your Documents and Containers to fit the use-cases, not vice-versa**
  - Create a Spreadsheet (i.e. - **Excel**) with this information
  - Add a column for the Estimated Number of Operations per Day
  - Add a column for the RU charge; populate this value as you observe your prototype RU costs 
  - Add a calculated column: Operation Count * RU cost
  - Sum this column; strive for the lowest sum RU total
  - Identify your most expensive operations; refactor/improve in the next iteration


---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](0_table_of_contents.md) &nbsp; | &nbsp; [next](4_02_design_considerations.md) &nbsp;
