#!/bin/bash

# For now, just get the name.basics.tsv.gz file
# See https://datasets.imdbws.com
# Chris Joakim, 2021/02/13

echo "getting name.basics ..."
curl "https://datasets.imdbws.com/name.basics.tsv.gz" > name.basics.tsv.gz

# echo "getting title.akas ..."
# curl "https://datasets.imdbws.com/title.akas.tsv.gz" > title.akas.tsv.gz

# echo "getting title.basics ..."
# curl "https://datasets.imdbws.com/title.basics.tsv.gz" > title.basics.tsv.gz

# echo "getting title.crew ..."
# curl "https://datasets.imdbws.com/title.crew.tsv.gz" > title.crew.tsv.gz

# echo "getting title.episode ..."
# curl "https://datasets.imdbws.com/title.episode.tsv.gz" > title.episode.tsv.gz

# echo "getting title.principals ..."
# curl "https://datasets.imdbws.com/title.principals.tsv.gz" > title.principals.tsv.gz

# echo "getting title.ratings ..."
# curl "https://datasets.imdbws.com/title.ratings.tsv.gz" > title.ratings.tsv.gz


# -rw-r--r--   1 cjoakim  staff  594565669 Mar 28 08:35 name.basics.tsv
# -rw-r--r--   1 cjoakim  staff  192512637 Mar 28 08:42 name.basics.tsv.gz
# -rw-r--r--   1 cjoakim  staff  180553446 Mar 28 08:42 title.akas.tsv.gz
# -rw-r--r--   1 cjoakim  staff  110193951 Mar 28 08:42 title.basics.tsv.gz
# -rw-r--r--   1 cjoakim  staff   47307965 Mar 28 08:42 title.crew.tsv.gz
# -rw-r--r--   1 cjoakim  staff   25734728 Mar 28 08:42 title.episode.tsv.gz
# -rw-r--r--   1 cjoakim  staff  316585301 Mar 28 08:43 title.principals.tsv.gz
# -rw-r--r--   1 cjoakim  staff    5039069 Mar 28 08:43 title.ratings.tsv.gz

echo 'unzipping'

gunzip name.basics.tsv.gz
# gunzip title.akas.tsv.gz
# gunzip title.basics.tsv.gz
# gunzip title.crew.tsv.gz
# gunzip title.episode.tsv.gz
# gunzip title.principals.tsv.gz
# gunzip title.ratings.tsv.gz

wc name.basics.tsv
# 10713450 73652513 639294242 name.basics.tsv

echo 'done'
