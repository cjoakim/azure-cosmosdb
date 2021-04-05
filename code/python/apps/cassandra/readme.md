# Apache Cassandra and CosmosDB

## CosmosDB

- Native: https://docs.microsoft.com/en-us/azure/cosmos-db/cassandra-introduction
- MI: https://devblogs.microsoft.com/cosmosdb/preview-azure-managed-instance-for-apache-cassandra/
- CCX: https://devblogs.microsoft.com/cosmosdb/announcing-live-data-migration-from-cassandra-to-azure-cosmos-db/
- https://docs.microsoft.com/en-us/azure/cosmos-db/cassandra-support

## CQLSH

- See https://cassandra.apache.org/doc/latest/tools/cqlsh.html
- See **cqlsh_cosmos.sh** in this directory

### CREATE TABLE example

```
use travel
```

```
CREATE TABLE travel.airports(
  "code"       text,
  "name"       text,
  "city"       text,
  "country"    text,
  "tz_name"    text,
  "tz_num"     int,
  "lat"        double,
  "lon"        double,
  "alt"        int,
  PRIMARY KEY (code)     <--- also the Partition Key
);
```

```
...
  PRIMARY KEY (name, city) <--- Alternative, a Compound Key and Partition Key
);
```

- https://docs.microsoft.com/en-us/azure/cosmos-db/cassandra-partitioning
- https://docs.microsoft.com/en-us/azure/cosmos-db/cassandra-secondary-index

### CREATE TABLE and specify Throughput (RUs)

Defaults to 400 unless otherwise specified.

```
CREATE TABLE keyspaceName.tablename (user_id int PRIMARY KEY, lastname text)
    WITH cosmosdb_provisioned_throughput=1200
```

### Other

```
$ ./cqlsh_cosmos.sh

connecting to: cjoakimcosmoscass.cassandra.cosmos.azure.com
Connected to CosmosProd at cjoakimcosmoscass.cassandra.cosmos.azure.com:10350.
[cqlsh 5.0.1 | Cassandra 3.11.0 | CQL spec 3.4.4 | Native protocol v66]
Use HELP for help.

cjoakimcosmoscass@cqlsh:travel> SHOW VERSION
[cqlsh 5.0.1 | Cassandra 3.11.0 | CQL spec 3.4.4 | Native protocol v66]

cjoakimcosmoscass@cqlsh:travel> SHOW HOST
Connected to CosmosProd at cjoakimcosmoscass.cassandra.cosmos.azure.com:10350.

cjoakimcosmoscass@cqlsh:travel> help describe

    DESCRIBE [cqlsh only]

    (DESC may be used as a shorthand.)

        Outputs information about the connected Cassandra cluster, or about
        the data objects stored in the cluster. Use in one of the following ways:

    DESCRIBE KEYSPACES

        Output the names of all keyspaces.

    DESCRIBE KEYSPACE [<keyspacename>]

        Output CQL commands that could be used to recreate the given keyspace,
        and the objects in it (such as tables, types, functions, etc.).
        In some cases, as the CQL interface matures, there will be some metadata
        about a keyspace that is not representable with CQL. That metadata will not be shown.

        The '<keyspacename>' argument may be omitted, in which case the current
        keyspace will be described.

    DESCRIBE TABLES

        Output the names of all tables in the current keyspace, or in all
        keyspaces if there is no current keyspace.

    DESCRIBE TABLE [<keyspace>.]<tablename>

        Output CQL commands that could be used to recreate the given table.
        In some cases, as above, there may be table metadata which is not
        representable and which will not be shown.

    DESCRIBE INDEX <indexname>

        Output the CQL command that could be used to recreate the given index.
        In some cases, there may be index metadata which is not representable
        and which will not be shown.

    DESCRIBE MATERIALIZED VIEW <viewname>

        Output the CQL command that could be used to recreate the given materialized view.
        In some cases, there may be materialized view metadata which is not representable
        and which will not be shown.

    DESCRIBE CLUSTER

        Output information about the connected Cassandra cluster, such as the
        cluster name, and the partitioner and snitch in use. When you are
        connected to a non-system keyspace, also shows endpoint-range
        ownership information for the Cassandra ring.

    DESCRIBE [FULL] SCHEMA

        Output CQL commands that could be used to recreate the entire (non-system) schema.
        Works as though "DESCRIBE KEYSPACE k" was invoked for each non-system keyspace
        k. Use DESCRIBE FULL SCHEMA to include the system keyspaces.

    DESCRIBE TYPES

        Output the names of all user-defined-types in the current keyspace, or in all
        keyspaces if there is no current keyspace.

    DESCRIBE TYPE [<keyspace>.]<type>

        Output the CQL command that could be used to recreate the given user-defined-type.

    DESCRIBE FUNCTIONS

        Output the names of all user-defined-functions in the current keyspace, or in all
        keyspaces if there is no current keyspace.

    DESCRIBE FUNCTION [<keyspace>.]<function>

        Output the CQL command that could be used to recreate the given user-defined-function.

    DESCRIBE AGGREGATES

        Output the names of all user-defined-aggregates in the current keyspace, or in all
        keyspaces if there is no current keyspace.

    DESCRIBE AGGREGATE [<keyspace>.]<aggregate>

        Output the CQL command that could be used to recreate the given user-defined-aggregate.

    DESCRIBE <objname>

        Output CQL commands that could be used to recreate the entire object schema,
        where object can be either a keyspace or a table or an index or a materialized
        view (in this order).
```

---

### DESCRIBE KEYSPACES

```
cjoakimcosmoscass@cqlsh:travel> DESCRIBE KEYSPACES

system_schema  system_auth  system  system_distributed  system_traces  travel

```

### DESCRIBE KEYSPACE travel

```
cjoakimcosmoscass@cqlsh:travel> DESCRIBE KEYSPACE travel

CREATE KEYSPACE travel WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;

CREATE TABLE travel.airports (
    code text PRIMARY KEY,
    alt int,
    city text,
    country text,
    lat double,
    lon double,
    name text,
    tz_name text,
    tz_num int
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND cdc = false
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 0
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 3600000
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';
```

### DESCRIBE TABLE travel.airports

```
cjoakimcosmoscass@cqlsh:travel> DESCRIBE TABLE travel.airports

CREATE TABLE travel.airports (
    code text PRIMARY KEY,
    alt int,
    city text,
    country text,
    lat double,
    lon double,
    name text,
    tz_name text,
    tz_num int
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND cdc = false
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.0
    AND default_time_to_live = 0
    AND gc_grace_seconds = 0
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 3600000
    AND min_index_interval = 128
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';
```

---

## Queries

- See https://docs.datastax.com/en/cql-oss/3.3/cql/cql_reference/cqlSelect.html

```
SELECT * | select_expression | DISTINCT partition 
FROM [keyspace_name.] table_name 
[WHERE partition_value
   [AND clustering_filters 
   [AND static_filters]]] 
[ORDER BY PK_column_name ASC|DESC] 
[LIMIT N]
[ALLOW FILTERING]
```

### SELECT * FROM travel.airports where code = 'CLT';

```
cjoakimcosmoscass@cqlsh:travel> SELECT * FROM travel.airports where code = 'CLT';

 code | name                   | city      | country       | tz_name          | tz_num | lat    | lon       | alt
------+------------------------+-----------+---------------+------------------+--------+--------+-----------+-----
  CLT | Charlotte Douglas Intl | Charlotte | United States | America/New_York |     -5 | 35.214 | -80.94314 | 748

```

---

## DESCRIBE CLUSTER and Key Ranges

```
cjoakimcosmoscass@cqlsh> use travel;
cjoakimcosmoscass@cqlsh:travel> DESCRIBE CLUSTER

Cluster: CosmosProd
Partitioner: Murmur3Partitioner

Range ownership:
                    -4682635034095501568  [40.78.226.21]
                    -6385411410130229408  [40.78.226.21]
                    -6953003535475138688  [40.78.226.21]
                    -8088187786164957248  [40.78.226.21]
                    -7236799598147593328  [40.78.226.21]
                    -7520595660820047968  [40.78.226.21]
                    -8939575974182321168  [40.78.226.21]
                     8655779911509866512  [40.78.226.21]
                     8088187786164957232  [40.78.226.21]
                     7520595660820047952  [40.78.226.21]
                     6953003535475138672  [40.78.226.21]
                     6385411410130229392  [40.78.226.21]
                     5817819284785320112  [40.78.226.21]
                     5250227159440410832  [40.78.226.21]
                     4682635034095501552  [40.78.226.21]
                     4115042908750592272  [40.78.226.21]
                     3547450783405682992  [40.78.226.21]
                    -7804391723492502608  [40.78.226.21]
                     2412266532715864432  [40.78.226.21]
                     1844674407370955152  [40.78.226.21]
                     1277082282026045872  [40.78.226.21]
                      709490156681136592  [40.78.226.21]
                      141898031336227312  [40.78.226.21]
                     -425694094008681968  [40.78.226.21]
                     -993286219353591248  [40.78.226.21]
                    -1560878344698500528  [40.78.226.21]
                    -2128470470043409808  [40.78.226.21]
                    -2696062595388319088  [40.78.226.21]
                    -3263654720733228368  [40.78.226.21]
                    -3831246846078137648  [40.78.226.21]
                    -4398838971423046928  [40.78.226.21]
                    -4966431096767956208  [40.78.226.21]
                    -5534023222112865488  [40.78.226.21]
                    -5817819284785320128  [40.78.226.21]
                    -4115042908750592288  [40.78.226.21]
                    -8371983848837411888  [40.78.226.21]
                     2979858658060773712  [40.78.226.21]
                     3263654720733228352  [40.78.226.21]
                    -8655779911509866528  [40.78.226.21]
                    -6101615347457774768  [40.78.226.21]
                     8939575974182321152  [40.78.226.21]
                     8371983848837411872  [40.78.226.21]
                     7804391723492502592  [40.78.226.21]
                     7236799598147593312  [40.78.226.21]
                     6669207472802684032  [40.78.226.21]
                     6101615347457774752  [40.78.226.21]
                     5534023222112865472  [40.78.226.21]
                     4966431096767956192  [40.78.226.21]
                     4398838971423046912  [40.78.226.21]
                     3831246846078137632  [40.78.226.21]
                    -6669207472802684048  [40.78.226.21]
                     2696062595388319072  [40.78.226.21]
                     2128470470043409792  [40.78.226.21]
                     1560878344698500512  [40.78.226.21]
                      993286219353591232  [40.78.226.21]
                      425694094008681952  [40.78.226.21]
                     -141898031336227328  [40.78.226.21]
                     -709490156681136608  [40.78.226.21]
                    -1277082282026045888  [40.78.226.21]
                    -1844674407370955168  [40.78.226.21]
                    -2412266532715864448  [40.78.226.21]
                    -2979858658060773728  [40.78.226.21]
                    -3547450783405683008  [40.78.226.21]
                    -5250227159440410848  [40.78.226.21]

```