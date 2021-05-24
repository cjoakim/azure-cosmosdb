#!/bin/bash

# Shell script to see if there are newer Maven libs than defined in the pom.xml file.
# Chris Joakim, Microsoft, 2018/10/23

mvn versions:display-dependency-updates
