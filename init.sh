#!/usr/bin/env bash

echo Initializing Brewery Metrics Gateway prerequisites...

LOCAL_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# enable python3 virtual environment
python3 -m venv "$LOCAL_PATH"/.venv
source "$LOCAL_PATH"/.venv/bin/activate

# add requirements
python3 -m ensurepip --upgrade
pip3 install --upgrade pip # setuptools wheel cython
pip3 install -r requirements.txt
