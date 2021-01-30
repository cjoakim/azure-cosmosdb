#!/bin/bash

# Bash script to create, populate, and activate the python virtual environment
# for this project with pyenv.
# Chris Joakim, 2020/10/12

# These are the only two values that need to change between projects:
venv_name="slfunc"
python_version="3.7.9"

display_help() {
    echo "script options:"
    echo "  ./pyenv.sh activate"
    echo "  ./pyenv.sh create"
}

activate() {
    echo '=== setting pyenv local ...'
    pyenv local $venv_name
}

create() {
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
}

arg_count=$#

if [ $arg_count -gt 0 ]
then
    if [ $1 == "activate" ] 
    then
        activate
    fi

    if [ $1 == "create" ] 
    then
        create
    fi
else
    display_help
fi
