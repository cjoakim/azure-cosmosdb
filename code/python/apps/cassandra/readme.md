# Apache Cassandra and CosmosDB

## CosmosDB

- Native: https://docs.microsoft.com/en-us/azure/cosmos-db/cassandra-introduction
- MI: https://devblogs.microsoft.com/cosmosdb/preview-azure-managed-instance-for-apache-cassandra/
- CCX: https://devblogs.microsoft.com/cosmosdb/announcing-live-data-migration-from-cassandra-to-azure-cosmos-db/

## CQLSH

- See https://cassandra.apache.org/doc/latest/tools/cqlsh.html
- See **cqlsh_cosmos.sh** in this directory

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