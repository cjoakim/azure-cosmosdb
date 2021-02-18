#!/bin/bash

# Execute the main Program via "mvn exec:java".
# Chris Joakim, Microsoft, 2021/02/18

class="org.cjoakim.azure.cosmos.sql.App"

mvn exec:java -Dexec.mainClass=$class -Dexec.args="point_read dev airports CLT xxx"
