#!/usr/bin/env bash

echo Initializing Brewery Metrics Gateway prerequisites...

LOCAL_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PYTHON_BIN="python3"

# create/reset python3 virtual environment
rm -fr $LOCAL_PATH/.venv
$PYTHON_BIN -m venv "$LOCAL_PATH"/.venv
source "$LOCAL_PATH"/.venv/bin/activate

# add requirements
python3 -m ensurepip --upgrade
pip3 install --upgrade pip
pip3 install -r requirements.txt
