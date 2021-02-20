#!/bin/bash

# See https://datasets.imdbws.com
# Chris Joakim, 2021/02/20

echo 'removing output files ...'
rm *.gz
rm *.tsv

echo "getting name.basics ..."
curl "https://datasets.imdbws.com/name.basics.tsv.gz" > name_basics.tsv.gz

echo "getting title.basics ..."
curl "https://datasets.imdbws.com/title.basics.tsv.gz" > title_basics.tsv.gz

echo 'unzipping ...'
gunzip name_basics.tsv.gz
gunzip title_basics.tsv.gz

echo 'creating smaller files for subsequent processing ...'

wc name_basics.tsv
wc title_basics.tsv

head -1000000 name_basics.tsv > name_basics_small.tsv
head -700000 title_basics.tsv > title_basics_small.tsv

wc name_basics_small.tsv
wc title_basics_small.tsv

ls -al | grep tsv

echo 'done'

# Script output:
# unzipping ...
# creating smaller files for subsequent processing ...
#  10729855 73763936 640327925 name_basics.tsv
#  7634823 103758168 651769914 title_basics.tsv
#  1000000 7058040 75239827 name_basics_small.tsv
#   700000 9407795 57167635 title_basics_small.tsv
# -rw-r--r--  1 cjoakim  staff  640327925 Feb 20 07:32 name_basics.tsv
# -rw-r--r--  1 cjoakim  staff   75239827 Feb 20 07:32 name_basics_small.tsv
# -rw-r--r--  1 cjoakim  staff  651769914 Feb 20 07:32 title_basics.tsv
# -rw-r--r--  1 cjoakim  staff   57167635 Feb 20 07:32 title_basics_small.tsv
# done
