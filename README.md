# Brewery Metrics Gateway

Let's capture your Brewery Metrics from your connected devices and forward them to multiple supported platforms.

## Overview

This projects aims at proposing a basic modular architecture to synchronize your Brewery Metrics from your connected devices to different external fermentation tracking systems.

Since the metrics data format is not standardized, the tool will manage the data transformation for you.

Design is decoupled in 2 concepts:

- The gateway **handlers** that receives periodic requests from your connected devices
- The gateway **forwarders** that converts and send your metrics to target tracking systems 

Currently, it supports the following:

- Gateway Handlers:
  - **BrewCreator**: Graviator, Ferminator, Fermcubator devices
- Gateway Forwarders:
  - **Grainfather** (as a Fermentor custom device)
  - **Littlebock** (as a iSpindel device)
  - BrewFather: to come...
  - Prometheus ? (if requested)



> **Note**: there are ways of improvement to manage and route specific devices data to specific forwarders... suggestions and inputs (data format and test endpoints) are welcome !

> **Warning**: as supported connected devices or tracking systems does not support authentication, there is no security layer implemented.



## Prerequisites

Create the python virtual environment using:

```shell
./init.sh
```



## Configure

Edit the `config.yaml` file as in the example below:

```yaml
## The gateway server configuration
gateway:

  ## The IP to listen to (defaults to 0.0.0.0 to listen on all interfaces).
  host: "0.0.0.0"
  ## The port to listen to.
  port: "8080"

## The gateway handlers configuration to receive data from the gateway.
## Just comment out the handlers to disable
handlers:

  ## The BrewCreator handler to receive metrics from following connected devices:
  ## - Graviator
  ## - Ferminator (or Fermcubator)
  brewCreator:
    ## The path to receive requests from BrewCreator
    path: /brewCreator

## The gateway forwarders configuration to send metrics to external fermentation tracking systems among:
## - grainfather
## - littlebock
## - brewfather (to come)
forwarders:

  ## The Grainfather server to forward data.
  grainfather:
    serverUrl: https://community.grainfather.com/iot/<ID>/custom 

  ## The Littlebock server to forward data.
  littlebock:
    serverUrl: http://www.littlebock.fr/api/log/ispindle/<ID1>/<ID2> 
```

> You can pretty easily add handlers/forwarders or comment-out the one you don't need


## Run as a service

> **Note**: This only supports **Linux** (systemd) services, otherwise, please check the "Run as a standalone process" section.

Configure the `service/brewery-metrics-gateway.service` template file if needed (user and paths are automatically injected).
Install the service to the system using:

```shell
./service/install.sh
```

> It will create a symbolic link from this file to `systemd`.

Run the service using:

```shell
systemctl start brewery-metrics-gateway
```

> The service should now be started and will restart the process in case of failure or system reboot.


## Run as a standalone process

If you want to start the process manually for testing purpose, you can run:

```shell
./start.sh
```

> The process will run in foreground by default, so it will stop when closing your terminal.
> For production, it is recommended to launch it as a service.



## Integration with connected device

Once the gateway is running, you can go to your connected device, and fill the gateway server address.

### BrewCreator.com

Go to Devices, select your device, and go to "Device" tab, then open "Integration" dropdown list and fill the cloud URL with something like:
 `http://<gateway.host>:<gateway.port>/<handlers.brewCreator.path>/<optionalDeviceName>` 

Save, and wait for next quarter to start receiving data (you should see the requests popping in the `app.log` file)