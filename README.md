# Brewery Metrics Gateway

Let's capture your Brewery Metrics from your connected devices and forward them to multiple supported platforms.

## Overview

This projects aims at proposing a basic modular architecture to synchronize your Brewery Metrics from your connected devices to different external fermentation tracking systems.

Since the metrics data format is not standardized, the tool will manage the data transformation for you.

Design is decoupled in 2 concepts:

- The gateway **handlers** that receive periodic requests from your connected devices
- The gateway **forwarders** that convert and send your metrics to target tracking systems 

Currently, it supports the following:

- Gateway Handlers:
  - **BrewCreator**: Graviator, Ferminator, Fermcubator devices
- Gateway Forwarders:
  - **Grainfather** (as a Fermentor custom device)
  - **Littlebock** (as a iSpindel device)
  - BrewFather: to come...
  - Prometheus ? (if requested)



> **Note**: there are ways of improvement to:
>
> - manage and route specific devices data to specific forwarders...
> - support scheduled pulls from a Prometheus server
>
> ==> suggestions and inputs (data format and test endpoints) are welcome (see Issue Tracker section).

> **Warning**: as supported connected devices or tracking systems does not support authentication, there is no security layer implemented.



## Prerequisites

This tool requires **Python 3.9+** to ensure maximum backward compatibility, however most recent versions are not automatically tested yet.

Create the python virtual environment using:

```shell
./init.sh
```



## Configuration

Edit the `config.yaml` file as in the example below:

```yaml
## The gateway server configuration
gateway:

  ## The IP to listen to (defaults to 0.0.0.0 to listen on all interfaces).
  #host: "0.0.0.0"
  ## The port to listen to.
  port: 8080

## The gateway handlers configuration to receive data from the gateway.
## Just comment out the handlers to disable
handlers:

  ## The BrewCreator handler to receive metrics from following connected devices:
  ## - Graviator
  ## - Ferminator (or Fermcubator)
  brewCreator:
    ## The path to receive requests from BrewCreator
    path: /brewCreator
    #class_name: BrewCreatorHandler

## The gateway forwarders configuration to send metrics to external fermentation tracking systems among:
## - grainfather
## - littlebock
## - brewfather (to come)
forwarders:

  ## The Grainfather server to forward data.
  grainfather:
    server_url: https://community.grainfather.com/iot/<ID>/custom
    #class_name: GrainfatherForwarder

  ## The Littlebock server to forward data.
  littlebock:
    server_url: http://www.littlebock.fr/api/log/ispindle/<ID1>/<ID2>
    #class_name: LittlebockForwarder
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

Save, and wait for next quarter (sometimes more) to start receiving data.
You should see the requests activity popping in the `app.log` file



## Issue Tracker

Feel free to vote for existing Bugs or Feature requests in the Github [issues](https://github.com/donatelloOo/brewery-metrics-gateway/issues), or enter new ones:

- [Bug tickets](https://github.com/donatelloOo/brewery-metrics-gateway/issues/new?template=bug_report.md)
- [Feature requests](https://github.com/donatelloOo/brewery-metrics-gateway/issues/new?template=feature_request.md)



## Credits

Credits to https://github.com/PaulLesur/transfer-hose that initiated a project to pull and forward metrics from a Prometheus server to Littlebock.