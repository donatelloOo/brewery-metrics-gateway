#!/usr/bin/env python3

from argparse import Namespace
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import json
import logging
from logging import Logger
from pydantic import ValidationError
from typing import Dict

from model.config import Config
from model.handler import Handler
from model.forwarder import Forwarder
from model.utils import read_yaml, parse_args

# Global variables
config: Config
path2handlerConf: Dict[str, Config.HandlerConfig]
logger: Logger


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
            handler_class: type[Handler] = handler_conf.class_type  # type: ignore
            metric_data = handler_class.transform(handler_conf, data)

            # Forward metric to external tracking systems
            for fw_conf in config.forwarders.values():
                # TODO implement per device routing logic
                fw_class: type[Forwarder] = fw_conf.class_type  # type: ignore
                fw_class.send(fw_conf, metric_data)

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
        except Exception as e:
            logger.error(f"Processing failed: {e}")
            self.send_response(500)


def run(server_class=HTTPServer,
        handler_class=GatewayHttpRequestHandler,
        host="0.0.0.0", port=8080):
    server_address = (host, port)
    # Create an HTTP server object and bind it to the specified port and host
    httpd = server_class(server_address=server_address, RequestHandlerClass=handler_class)  # type: ignore
    logger.info(f"Server started on port {host}:{port}")
    httpd.serve_forever()


def build_config(config_file: str, args: Namespace):
    global config, path2handlerConf
    try:
        # load config
        yaml_config = read_yaml(config_file)
        if args.ip:
            yaml_config['gateway']['host'] = args.ip
        if args.port:
            yaml_config['gateway']['port'] = args.port
        config = Config(**yaml_config)

        # pre-compute fast-access maps
        path2handlerConf = {
            handler_conf.path: handler_conf
            for handler_conf in config.handlers.values()
        }
    except ValidationError as err:
        logger.error(f"Error when parsing config: {err}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error when parsing config: {e}")
        raise e


def main():
    global logger
    args = parse_args()

    # Logging configuration
    logging.basicConfig(
        level=args.logLevel,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(args.logFile),  # log to file
            logging.StreamHandler()  # log to console
        ]
    )
    logger = logging.getLogger("gateway")

    # load config and pre-compute related resources
    build_config(config_file=args.config, args=args)

    # start gateway server
    run(HTTPServer, GatewayHttpRequestHandler, config.gateway.host, config.gateway.port)


if __name__ == '__main__':
    main()
