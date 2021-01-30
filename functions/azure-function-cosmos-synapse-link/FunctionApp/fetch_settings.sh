#!/bin/bash

# Download the settings for a named Azure Function.
# Chris Joakim, Microsoft, 2020/10/10

app_name="cjoakimsynapse2f"

echo 'fetching settings for function app named: '$app_name

func azure functionapp fetch-app-settings $app_name

echo 'done'
