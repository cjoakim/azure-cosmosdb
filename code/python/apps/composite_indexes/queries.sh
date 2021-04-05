#!/bin/bash

# Bash script to query the two containers with the same data, but different indexing.
# Chris Joakim, 2021/04/05

# echo ''
# echo '==='
# python main.py named_query dev postalcodes1 nh-us-manchester
# echo ''
# python main.py named_query dev postalcodes2 nh-us-manchester

echo ''
echo '==='
python main.py named_query dev postalcodes1 city-state
echo ''
python main.py named_query dev postalcodes2 city-state



echo 'done'
