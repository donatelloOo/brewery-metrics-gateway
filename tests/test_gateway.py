import os
import socket
import subprocess
import time

import pytest


def test_gateway_startup():
    test_port = 8888

    # start gateway in background using shell script
    script_path = os.path.abspath("start.sh")
    server_process = subprocess.Popen(
        [script_path, "-c", "tests/config_test.yaml"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    time.sleep(5)

    assert is_port_open(test_port)


def is_port_open(port: int, host: str = "127.0.0.1") -> bool:
    """
    Vérifie si un port est ouvert et accessible.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(1)
            s.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False
