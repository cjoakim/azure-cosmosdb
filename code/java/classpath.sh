#!/bin/bash

# This script calculates the maven CLASSPATH and produces the
# 'classpath' file, which can be sourced from a bash shell script.
#
# Chris Joakim, Microsoft, 2020/11/15

mvn dependency:build-classpath -Dmdep.outputFile=classpath.txt

echo 'executing classpath.py to generate classpath file'
python3 classpath.py classpath > classpath

echo 'executing classpath.py to generate jar_contents script'
python3 classpath.py jar_contents > jar_contents.sh
