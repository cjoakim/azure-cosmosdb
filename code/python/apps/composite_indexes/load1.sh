#!/bin/bash

# Bash script to load the coll1 container.
# Chris Joakim, 2021/04/07

infile="data/postal_codes_us_filtered.csv"

python main.py load_container dev coll1 data/postal_codes_us_filtered.csv 0 99999 > tmp/load_coll1.txt

echo 'done'
