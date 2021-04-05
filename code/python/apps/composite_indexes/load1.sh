#!/bin/bash

# Bash script to load the postalcodes1 container.
# Chris Joakim, 2021/04/05

infile="data/postal_codes_us_filtered.csv"

python main.py load_container dev postalcodes1 $infile 0 99999 > tmp/load_postalcodes1.txt

echo 'done'
