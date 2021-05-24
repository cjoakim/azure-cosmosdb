#!/bin/bash

# Shell script to see if there are newer Maven libs than defined in the pom.xml file.
# Chris Joakim, Microsoft, Chris Joakim, Microsoft, 2021/02/18

mvn versions:display-plugin-updates

mvn versions:display-dependency-updates

# This script produces output like the following:
# [INFO] The following dependencies in Dependencies have newer versions:
# [INFO]   junit:junit ........................................... 4.11 -> 4.13.2
# [INFO]   org.apache.commons:commons-lang3 ........................ 3.10 -> 3.11
# [INFO]   org.apache.logging.log4j:log4j-api .................. 2.11.1 -> 2.14.0
# [INFO]   org.apache.logging.log4j:log4j-slf4j-impl ........... 2.13.0 -> 2.14.0
# [INFO]   org.slf4j:slf4j-jdk14 ......................... 1.7.28 -> 2.0.0-alpha1
# [INFO]
