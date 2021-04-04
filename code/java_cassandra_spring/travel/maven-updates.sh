#!/bin/bash

# Shell script to see if there are newer Maven libs than defined in the pom.xml file.
# Chris Joakim, Microsoft, 2021/03/20

mvn dependency:tree

mvn versions:display-plugin-updates

mvn versions:display-dependency-updates
