#!/usr/bin/env bash

echo Installing Brewery Metrics Gateway Service...

BASE_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." &> /dev/null && pwd)
SERVICE_FILE="$BASE_PATH"/service/brewery-metrics-gateway.service
CURRENT_USER=$(id -un)

sed -i -r "s|User=.*|User=$CURRENT_USER|" $SERVICE_FILE
sed -i -r "s|WorkingDirectory=.*|WorkingDirectory=$BASE_PATH|" $SERVICE_FILE
sed -i -r "s|ExecStart=.*|ExecStart=$BASE_PATH/start.sh|" $SERVICE_FILE

# Install as a service by creating a symbolic link to the system
sudo ln -sf  $SERVICE_FILE /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start brewery-metrics-gateway
