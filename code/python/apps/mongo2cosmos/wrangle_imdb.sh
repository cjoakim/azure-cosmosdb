#!/bin/bash

# Bash shell script to read the IMDb TSV files and produce corresponding output
# files in mongoexport format, to simulate an export from a "source" database.
# Chris Joakim, Microsoft, 2021/02/20

python wrangle_imdb.py tsv_to_mongoexport data/imdb/name_basics_small.tsv  data/mongo/name_basics_small_source.json

python wrangle_imdb.py tsv_to_mongoexport data/imdb/title_basics_small.tsv data/mongo/title_basics_small_source.json

echo 'done'

# Script output:
#
# $ ./wrangle_imdb.sh
# tsv_to_mongoexport: data/imdb/name_basics_small.tsv -> data/mongo/name_basics_small_source.json
# col_names: ['nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession', 'knownForTitles']
# elapsed: 9.98999810218811
# infile:  data/imdb/name_basics_small.tsv
# outfile: data/mongo/name_basics_small_source.json
# 999999
# tsv_to_mongoexport: data/imdb/title_basics_small.tsv -> data/mongo/title_basics_small_source.json
# col_names: ['tconst', 'titleType', 'primaryTitle', 'originalTitle', 'isAdult', 'startYear', 'endYear', 'runtimeMinutes', 'genres']
# elapsed: 7.944829940795898
# infile:  data/imdb/title_basics_small.tsv
# outfile: data/mongo/title_basics_small_source.json
# 699999
# done
