#!/bin/bash

# Bash script to load the coll2 container.
# Chris Joakim, 2021/04/07

infile="data/postal_codes_us_filtered.csv"

python main.py load_container compidx coll2 data/postal_codes_us_filtered.csv 0 99999 > tmp/load_coll2.txt

echo 'done'
