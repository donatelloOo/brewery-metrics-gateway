import argparse
import importlib
import ipaddress
import logging
import pkgutil
import re
import sys
from typing import TypeVar, Type

import yaml

T = TypeVar('T')  # generic type for base class

# Global variables
logger = logging.getLogger(__name__)


def ip_or_hostname_type(s) -> str:
    # check if it's a valid IP address (IPv4 ou IPv6)
    try:
        return str(ipaddress.ip_address(s))
    except ValueError:
        pass

    # check if it's a valid hostname
    if not re.match(
            r'^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])'
            r'(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*$',
            s
    ):
        raise argparse.ArgumentTypeError(
            f"'{s}' is not a valid IP address (IPv4/IPv6) or a valid hostname"
        )
    return s


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
    return None  # type: ignore


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Brewery Metrics Gateway.")
    parser.add_argument("-c", "--config", type=str, default="config.yaml",
                        help="The YAML configuration file to use.")
    parser.add_argument("-i", "--ip", type=ip_or_hostname_type,
                        help="The default IP address or hostname to listen to (overrides config).")
    parser.add_argument("-p", "--port", type=int,
                        help="The default port to listen to (overrides config).")
    parser.add_argument("-f", "--logFile", type=str, default="app.log",
                        help="The log file to write.")
    parser.add_argument("-l", "--logLevel", type=str, default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        help="The log level to use.")
    return parser.parse_args()
