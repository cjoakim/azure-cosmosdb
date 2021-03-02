#!/bin/bash

# Bash shell script to export each source collection via mongoexport.
#
# Database Name: {{ dbname }}
# Generated on:  {{ gen_timestamp }}

{% for c in collections %}
mongoexport \
  --host $MONGODB_HOST \
  --port $MONGODB_PORT \
  -d {{ dbname }} \
  -u $MONGODB_USER \
  -p $MONGODB_PASS \
  -c {{ c['name'] }} \
  --ssl \
  --out data/mongo/{{ dbname }}_{{ c['name'] }}_source.json
{% endfor %}

echo 'done'
