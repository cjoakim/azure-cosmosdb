#!/bin/bash

# Bash shell script to execute mongoexport file transformations
# from "source" to "target" database format.
#
# Database Name: {{ dbname }}
# Generated on:  {{ gen_timestamp }}

# Execute the transformations for the database:
{% for c in collections %}
python transform_mongoexports.py transform \
  {{ c['name'] }} \
  data/mongo/{{ c['name'] }}_source.json \
  data/mongo/{{ c['name'] }}_target.json
{% endfor %}

# Verify the transformations for the database:
{% for c in collections %}
python transform_mongoexports.py verify_transformation \
  {{ c['name'] }} {{ c['count'] }} \
  data/mongo/{{ c['name'] }}_source.json \
  data/mongo/{{ c['name'] }}_target.json
{% endfor %}

echo 'done'
