#!/bin/bash

# Execute the main Program via "mvn exec:java".
# Chris Joakim, Microsoft, 2021/06/28

class="org.cjoakim.azure.cosmos.sql.App"

mvn exec:java -Dexec.mainClass=$class \
  -Dexec.args="select_distinct dev airports"
