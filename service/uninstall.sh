#!/usr/bin/env bash

echo Uninstalling Brewery Metrics Gateway Service...

# Install as a service by creating a symbolic link to the system
sudo systemctl stop brewery-metrics-gateway
sudo rm /etc/systemd/system/brewery-metrics-gateway.service
sudo systemctl daemon-reload
