#!/bin/bash

# Bash script to load the two containers with the same data, but different indexing.
# Chris Joakim, 2021/04/04

infile="data/postal_codes_us_filtered.csv"

python main.py load_container dev postalcodes1 $infile 0 99999 > tmp/load_postalcodes1.txt

python main.py load_container dev postalcodes2 $infile 0 99999 > tmp/load_postalcodes2.txt

echo 'done'
