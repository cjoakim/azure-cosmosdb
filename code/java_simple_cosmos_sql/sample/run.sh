#!/bin/bash

# Execute the main Program via "mvn exec:java".
# Chris Joakim, Microsoft, 2021/02/19

class="org.cjoakim.azure.cosmos.sql.App"

mvn exec:java -Dexec.mainClass=$class \
  -Dexec.args="point_read dev airports SFO 895014e0-1d52-40f6-8ae2-f9dcb0119961 5"
