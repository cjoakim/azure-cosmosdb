#!/bin/bash

# Bash shell script to query the CosmosDB Graph database
# Chris Joakim, Microsoft, 2020/11/11

dotnet run process_gremlin_commands ../data/gremlin/gremlin_queries.txt 

echo 'done'


# 0 Command: g.V().count()
# Result:
# 1147

# x-ms-status-code           : 200
# x-ms-total-server-time-ms] : 34.4301
# x-ms-total-request-charge] : 3.75

# ---
# 1 Command: g.E().count()
# Result:
# 3538
