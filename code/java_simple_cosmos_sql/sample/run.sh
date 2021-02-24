#!/bin/bash

# Execute the main Program via "mvn exec:java".
# Chris Joakim, Microsoft, 2021/02/24

class="org.cjoakim.azure.cosmos.sql.App"

mvn exec:java -Dexec.mainClass=$class \
  -Dexec.args="point_read dev airports PDT f9331886-a503-4fa7-b585-a134b24a5cdd 5"
