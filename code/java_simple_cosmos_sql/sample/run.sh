#!/bin/bash

class="org.cjoakim.azure.cosmos.sql.App"

mvn exec:java -Dexec.mainClass=$class -Dexec.args="xxx yyy zzz"
