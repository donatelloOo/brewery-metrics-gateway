#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler
import logging
import yaml
import json
import sys
import importlib
import pkgutil
from typing import Type, TypeVar

from pydantic import ValidationError

from model.handler import Handler
from model.forwarder import Forwarder
from model.config import Config

# Set the default host name and port number
default_host = "0.0.0.0"
default_port = 8080
config: Config = None
path2handlerConf = {}
path2handlerClass = {}
name2forwarderClass = {}

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('app.log'),  # log to file
        logging.StreamHandler()  # log to console
    ]
)
logger = logging.getLogger("gateway")


# Define the BrewCreator HTTP request handler
class GatewayHttpRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """
        For future usage of external scrappers (like prometheus).
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        """
        Receives Handlers POST requests.
        """
        try:
            # Read POST data
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            # Log POST request (including data)
            logger.debug(
                f"POST request received: Path={self.path}, "
                f"Headers={dict(self.headers)}, "
                f"Data={data if data else 'None'}"
            )

            # Transform device metric to standard metric according to requested handler
            base_path = f"/{self.path.split('/')[1]}"
            handler_conf = path2handlerConf.get(base_path)
            handler_class: type[Handler] = path2handlerClass.get(base_path)
            metric_data = handler_class.transform(handler_conf, data)

            # Forward metric to external tracking systems
            for fw_name, fw_class in name2forwarderClass.items():
                # TODO implement per device routing logic
                fw_class.send(config.forwarders[fw_name], metric_data)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            self.send_response(500)


def read_yaml(file_yaml) -> dict:
    """
    Load a YAML file.
    """
    with open(file_yaml, 'r', encoding="utf-8") as fd:
        try:
            return yaml.safe_load(fd)
        except yaml.YAMLError as e:
            print(f"Error when reading yaml file: {e}")
            sys.exit(1)


T = TypeVar('T')  # generic type for base class


def find_class(package_name: str, base_class: Type[T], class_name: str, recursive: bool = True) -> Type[T]:
    """
    Find first class matching given `class_name` in a package (and all sub-packages if `recursive=True`)
    that inherits the `base_class`.

    Args:
        package_name (str): Package name to explore.
        base_class (Type[T]): Base class or interface to filter on.
        class_name (str): Class name to find
        recursive (bool): True to explore sub-packages. Default: True.

    Returns:
        Type[T]: The class found or None.

    Raises:
        ImportError: If package does not exist.
    """
    try:
        package = importlib.import_module(package_name)
    except ImportError as e:
        raise ImportError(f"Package '{package_name}' cannot be found.") from e

    # iterate on all modules in package
    for _, module_name, is_pkg in pkgutil.iter_modules(package.__path__, prefix=f"{package_name}."):
        # skip if module is a sub-package and recursive=False
        if is_pkg and not recursive:
            continue
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue  # ignore non-importable modules

        # iterate on all classes in module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)

            # check if attribute is a class that inherits base class with same name
            if (isinstance(attr, type)
                    and issubclass(attr, base_class)
                    and attr != base_class  # exclude base class itself
                    and class_name == attr_name):
                # return first class matching
                return attr
    return None


def build_config(config_file: str = "config.yaml"):
    global config, path2handlerConf, path2handlerClass, name2forwarderClass
    try:
        # load config
        yaml_config = read_yaml(config_file)
        config = Config(**yaml_config)

        # pre-compute fast-access maps
        path2handlerConf = {
            handler_conf.path: handler_conf
            for handler_conf in config.handlers.values()
        }
        path2handlerClass = {
            handler_conf.path: find_class('handlers', Handler, handler_conf.class_name)
            for handler_name, handler_conf in config.handlers.items()
        }
        name2forwarderClass = {
            fw_name: find_class('forwarders', Forwarder, fw_conf.class_name)
            for fw_name, fw_conf in config.forwarders.items()
        }
    except ValidationError as err:
        logger.error(f"Error when parsing config: {err}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error when parsing config: {e}")
        sys.exit(1)


def run(server_class=HTTPServer, handler_class=GatewayHttpRequestHandler, host=default_host, port=default_port):
    server_address = (host, port)
    # Create an HTTP server object and bind it to the specified port and host
    httpd = server_class(server_address, handler_class)
    logger.info(f"Server started on port {host}:{port}")
    httpd.serve_forever()


if __name__ == '__main__':
    # load config and pre-compute related resources
    build_config()

    # start gateway server
    run(HTTPServer, GatewayHttpRequestHandler, config.gateway.host, config.gateway.port)
