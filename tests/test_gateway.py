import socket
import subprocess
import time


def test_gateway_startup():
    # start gateway in background using shell script
    port = 8888
    process = run_server(f'./gateway.py -c tests/config_test.yaml')

    try:
        # wait for port to be open
        wait_for_port(port)
        print(f"✅ Test passed: server started and port {port} is open.")
    except Exception as e:
        # terminate process and rethrow exception
        terminate_process(process)
        raise e
    else:
        # terminate process gracefully
        terminate_process(process)


def run_server(command: str, timeout: float = 5.0) -> subprocess.Popen:
    """
    Runs sub process and returns:
    - started process (or None if case of immediate failure).
    - an exception if startup failed, None otherwise.
    """
    process = subprocess.Popen(
        command,
        shell=True
    )

    # check that process started correctly (wait a short period)
    time.sleep(0.1)
    if process.poll() is not None:
        # process stopped immediately, capture exceptions
        raise ValueError(f"Process failed to start (exit code: {process.returncode})")

    return process


def is_port_open(port: int, host: str = "127.0.0.1", timeout: int = 10) -> bool:
    """
    Verify if a port is open.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(timeout)
            s.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError):
            return False


def wait_for_port(
        port: int,
        max_attempts: int = 10,
        attempt_delay: float = 1,
) -> None:
    """Wait for port to be open."""
    for _ in range(max_attempts):
        if is_port_open(port):
            return
        print(f"waiting for port {port} to be open...")
        time.sleep(attempt_delay)
    raise TimeoutError(f"Port {port} did not open after {max_attempts * attempt_delay:.1f} seconds")


def terminate_process(process: subprocess.Popen) -> None:
    """Gracefully stops a sub-process."""
    if process.poll() is None:  # if process still runs
        process.terminate()  # send SIGTERM
        try:
            process.wait(timeout=2.0)  # waits for graceful termination
        except subprocess.TimeoutExpired:
            process.kill()  # send SIGKILL
