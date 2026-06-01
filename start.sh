#!/bin/bash

# #!/usr/bin/env bash

echo Starting Brewery Metrics Gateway...

LOCAL_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# enable python virtual environment
source "$LOCAL_PATH"/.venv/bin/activate

# run gateway server (foreground)
exec "$LOCAL_PATH"/gateway.py "$@"

# run gateway server (background)
#nohup $LOCAL_PATH/gateway.py > $LOCAL_PATH/console.log 2>&1 &
#echo Server started in background.
#echo Logs available in: $LOCAL_PATH/console.log
