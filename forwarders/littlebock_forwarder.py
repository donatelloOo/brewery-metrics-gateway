import requests
import logging

from model.config import Config
from model.forwarder import Forwarder
from model.metric import MetricData

# Logger
logger = logging.getLogger(__name__)


# Define the BrewCreator handler
class LittlebockForwarder(Forwarder):

    @staticmethod
    def send(config: Config.ForwarderConfig, metric: MetricData) -> bool:
        """
        Send data to Littlebock endpoint.

        Expected format is:
        {
            "gravity": 1.034, // This must be numeric
            "temperature": 18, // This must be numeric
            "battery": 98 // This must be numeric
        }
        """
        data = {
            'gravity': metric.gravity,
            'temperature': metric.temperature,
            'battery': metric.battery,
        }
        logger.debug("Sending data: %s , %s", config.server_url, data)
        response = requests.post(config.server_url, data, timeout=10)

        if response.status_code == 200:
            if response.json().get('success'):
                logger.info(f"Update Success")
                return True
            else:
                logger.warning(response.json().get('message'))
                logger.debug(f"{response.status_code}: {response.json()}")
        else:
            logger.warning(f"Unmanaged response ({response.status_code}): {response.text}")
        return False
