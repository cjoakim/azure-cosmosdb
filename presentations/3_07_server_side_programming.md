# 3.07 - Server Side Programming

**CosmosDB Server-Side Programming is implemented in JavaScript**.

See https://docs.microsoft.com/en-us/azure/cosmos-db/stored-procedures-triggers-udfs

See the **code/server_side** directory of this repo.

## Stored Procedures

- Enables Atomic transactions
- Enables Batching
- Timeout limit of 5 seconds

###  ACID Transactions

- Atomicity, Consistency, Isolation, and Durability
- **Scoped to a Logical Partition Key**

### Examples

#### Hello World

```
function hello(prefix) {
    var response = getContext().getResponse();
    response.setBody("Hello at " + new Date().toISOString());
}
```

#### Creating History Documents

```
function createHistoryDoc(pk, id) {
    var collection = getContext().getCollection();
    var selfLink = collection.getSelfLink();
    var sql = "SELECT * FROM root r where r.pk = '" + pk + "' and r.id = '" + id + "'";
    var response = getContext().getResponse();
    var responseObj = {};
    responseObj['pk'] = pk;
    responseObj['sql'] = sql;

    var isAccepted = collection.queryDocuments(selfLink, sql,
        function (err, docs, options) {
            if (err) throw err;
            if (!docs || !docs.length) { 
                responseObj['message'] = 'document not found';
                response.setBody(JSON.stringify(responseObj));
            }
            else {
                var historyDoc = docs[0]; // prune and augment the found doc
                var date = new Date();
                delete historyDoc['id'];
                delete historyDoc['_attachments'];
                delete historyDoc['_etag'];
                delete historyDoc['_lsn'];
                delete historyDoc['_rid'];
                delete historyDoc['_self'];
                delete historyDoc['_ts']; 
                historyDoc['doctype'] = historyDoc['doctype'] + '_history';
                historyDoc['history_id_pk'] = '' + id + '|' + pk;
                historyDoc['history_date'] = date;
                historyDoc['history_epoc'] = date.getTime(); 
                historyDoc['Active'] = 0; 

                var created = collection.createDocument(selfLink, historyDoc,  
                    function (err, newDoc) { 
                        if (err) {
                            responseObj['message'] = 'error: ' + err.message;  
                        }  
                    });  
                responseObj['message'] = 'created: ' + created;
                response.setBody(JSON.stringify(responseObj));
            }
        });
    if (!isAccepted) throw new Error('The query was not accepted by the server.');
}
```

---

## User Defined Functions (UDFs)

- Enables you to **extend the SQL language** for your application
- Enables your SQL queries to read more fluently

### Definition of a UDF

```
function southEastUsa(pk) {
    return ["ATL", "CAE", "CLT", "GSP", "MIA", "MCO", "JAX", "RDU", "TPA"].includes(pk);
}
```

### Use of a UDF

```
SELECT c.pk, c.City, c.Name FROM c WHERE udf.southEastUsa(c.pk)
```

---

## Triggers

- They don't work as you might expect as in relational databases
  - They don't run automatically
  - Your client code has to request their invocation
  - Think of them as a remote reusable method
- Pre-triggers
- Post-triggers

### C# Example

#### Create the Trigger: trgPreValidateToDoItemTimestamp

```
await client.GetContainer("database", "container").Scripts.CreateTriggerAsync(
    new TriggerProperties
    {
        Id = "trgPreValidateToDoItemTimestamp",
        Body = File.ReadAllText("@..\js\trgPreValidateToDoItemTimestamp.js"),
        TriggerOperation = TriggerOperation.Create,
        TriggerType = TriggerType.Pre
    });
```

#### Use the Trigger

```
dynamic newItem = new
{
    category = "Personal",
    name = "Groceries",
    description = "Pick up strawberries",
    isComplete = false
};

await client.GetContainer("database", "container").CreateItemAsync(
    newItem, null, new ItemRequestOptions { 
        PreTriggers = new List<string> { "trgPreValidateToDoItemTimestamp" } });
```

---

## Links

- https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-write-stored-procedures-triggers-udfs
- https://docs.microsoft.com/en-us/azure/cosmos-db/how-to-use-stored-procedures-triggers-udfs

---

[toc](0_table_of_contents.md) &nbsp; |  &nbsp; [previous](3_06_sql.md) &nbsp; | &nbsp; [next](3_08_change_feed.md) &nbsp;
