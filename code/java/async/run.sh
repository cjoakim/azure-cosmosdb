#!/bin/bash

# Execute the main Program via "mvn exec:java".
# Chris Joakim, Microsoft, 2021/06/28

class="org.cjoakim.cosmos.App"

mvn exec:java -Dexec.mainClass=$class \
  -Dexec.args="xxx yyy zzz"

