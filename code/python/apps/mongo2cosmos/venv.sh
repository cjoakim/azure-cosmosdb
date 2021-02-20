#!/bin/bash

# Bash shell script to delete or create the Python Virtual Environment.
# Requires Python 3; version 3.7 or higher recommended.
# Chris Joakim, Microsoft, 2021/02/20

display_help() {
    echo "script options:"
    echo "  ./venv.sh delete"
    echo "  ./venv.sh create"
    echo "  ./venv.sh pip_list"
    echo "  ./venv.sh help"
}

delete_venv() {
    echo 'deleting previous venv...'
    rm -rf bin/
    rm -rf include/
    rm -rf lib/
    rm -rf man/
    echo 'done'
}

create_venv() {
    echo 'creating new venv ...'
    python3 -m venv .
    source bin/activate
    python3 --version
    pip3 --version

    # echo 'installing/upgrading pip3...'
    # pip3 install --upgrade pip
    # pip3 --version

    echo 'installing/upgrading pip-tools...'
    pip install --upgrade pip-tools

    echo 'pip-compile requirements.in ...'
    pip-compile --output-file requirements.txt requirements.in

    echo 'pip3 install requirements.txt ...'
    pip3 install -r requirements.txt

    pip3 list

    echo 'next: source bin/activate ; python3 --version'
    echo 'done'
}

pip_list() {
    echo 'pip_list ...'
    pip3 list --format=json
    echo 'done'
}

arg_count=$#

if [ $arg_count -gt 0 ]
then
    if [ $1 == "help" ] 
    then
        display_help
    fi

    if [ $1 == "delete" ] 
    then
        delete_venv
    fi

    if [ $1 == "create" ] 
    then
        create_venv
    fi

    if [ $1 == "pip_list" ] 
    then
        pip_list
    fi
else
    display_help
fi
