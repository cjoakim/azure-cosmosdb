#!/bin/bash

# Bash script to create, populate, and activate the python virtual environment
# for this project with pyenv.
# Chris Joakim, 2021/04/04

# These are the only two values that need to change between projects:
venv_name="compidx"
python_version="3.8.6"  # 3.7.9

echo '=== creating virtualenv '$venv_name
rm .python-version
pyenv virtualenv -f $python_version $venv_name

echo '=== python version'
python --version 

echo '=== setting pyenv local ...'
pyenv local $venv_name

echo '=== upgrade pip ...'
pip install --upgrade pip

echo '=== install pip-tools ...'
pip install pip-tools

echo '=== pip compile ...'
pip-compile

echo '=== pip install ...'
pip install -r requirements.txt

echo '=== pip list ...'
pip list

echo '=== .python-version ...'
cat .python-version

echo 'done'
