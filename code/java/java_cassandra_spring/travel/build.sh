#!/bin/bash

# Builds this Spring Boot app; creates an "uber jar".
# Chris Joakim, 2021/04/04

rm target/travel-*.jar

mvn clean compile package
