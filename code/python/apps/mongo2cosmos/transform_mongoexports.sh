#!/bin/bash

# Bash shell script to execute mongoexport file transformations fro
# "source" to "target" database format.
# Chris Joakim, Microsoft, 2021/02/20

python transform_mongoexports.py transform \
    name_basics \
    data/mongo/name_basics_small_source.json \
    data/mongo/name_basics_small_target.json

python transform_mongoexports.py transform \
    title_basics \
    data/mongo/title_basics_small_source.json \
    data/mongo/title_basics_small_target.json

# pretty-print a row - original and transformed versions
head -1 data/mongo/title_basics_small_source.json | jq 
head -1 data/mongo/title_basics_small_target.json | jq 

echo 'done'

# Script output:
#
# $ ./transform_mongoexports.sh
# transform: name_basics -> data/mongo/name_basics_small_source.json -> data/mongo/name_basics_small_target.json
# xform_rule: name_basics
# infile:     data/mongo/name_basics_small_source.json
# outfile:    data/mongo/name_basics_small_target.json
# elapsed:    10.8701651096344
# transform: title_basics -> data/mongo/title_basics_small_source.json -> data/mongo/title_basics_small_target.json
# xform_rule: title_basics
# infile:     data/mongo/title_basics_small_source.json
# outfile:    data/mongo/title_basics_small_target.json
# elapsed:    8.407235145568848
# {
#   "_id": "603111b6076315a46b2fd611",
#   "seq": 1,
#   "tconst": "tt0000001",
#   "titleType": "short",
#   "primaryTitle": "Carmencita",
#   "originalTitle": "Carmencita",
#   "isAdult": "0",
#   "startYear": "1894",
#   "endYear": "\\N",
#   "runtimeMinutes": "1",
#   "genres": "Documentary,Short"
# }
# {
#   "_id": "603111b6076315a46b2fd611",
#   "seq": 1,
#   "tconst": "tt0000001",
#   "titleType": "short",
#   "primaryTitle": "Carmencita",
#   "originalTitle": "Carmencita",
#   "isAdult": "0",
#   "startYear": "1894",
#   "endYear": "\\N",
#   "runtimeMinutes": "1",
#   "genres": [
#     "Documentary",
#     "Short"
#   ],
#   "pk": "tt0000001"
# }
# done
