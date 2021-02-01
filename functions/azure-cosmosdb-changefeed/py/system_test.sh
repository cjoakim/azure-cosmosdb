#!/bin/bash

# Execute a system-test of this demonstration project.
# Chris Joakim, Microsoft, 2020/06/25

source bin/activate

dbname=dev

date > tmp/system_test_start.txt

echo 'truncating containers...'
python main.py truncate_container $dbname events 6000  > tmp/truncate_container_events.txt
python main.py truncate_container $dbname changes 6000 > tmp/truncate_container_changes.txt

echo 'populating CosmosDB and triggering the change-feed Azure Function...'
python main.py populate_cosmos $dbname events 5000 true > tmp/populate_cosmos.txt

echo 'querying the DB for possible changes to restore...'
python main.py pre_restore_query $dbname events changes Raleigh   > tmp/pre_restore_query_raleigh.txt
python main.py pre_restore_query $dbname events changes Charlotte > tmp/pre_restore_query_charlotte.txt
python main.py pre_restore_query $dbname events changes Davidson  > tmp/pre_restore_query_davidson.txt

# Next: look at the pre_restore_query files and identify a document with a given _ts to restore, then:
# python main.py restore dev events changes Raleigh 1592853174

date > tmp/system_test_finish.txt
echo 'done'
