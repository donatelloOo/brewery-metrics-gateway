import requests
import logging

from model.config import Config
from model.forwarder import Forwarder
from model.metric import MetricData, TemperatureUnit

# Logger
logger = logging.getLogger(__name__)


# Define the BrewCreator handler
class GrainfatherForwarder(Forwarder):

    @staticmethod
    def send(config: Config.ForwarderConfig, metric: MetricData) -> bool:
        """
        Send metric data to Grainfather endpoint.

        Expected format is:
        {
            "specific_gravity": 1.034, // This must be a numeric value
            "temperature": 18, // This must be numeric
            "unit": "celsius" || "fahrenheit" // Supply the unit that matches the temperature you are sending
        }
        """
        data = {
            'specific_gravity': metric.gravity,
            'temperature': metric.temperature,
            'unit': 'celsius' if metric.temperature_unit == TemperatureUnit.CELSIUS else 'fahrenheit'
        }
        logger.debug("Sending data: %s , %s", config.server_url, data)
        response = requests.post(config.server_url, data, timeout=10)

        if response.status_code in (200, 201):
            logger.info(f"Update Success")
            return True
        elif response.status_code == 422:
            logger.error(f"Invalid request: {response.text}")
        elif response.status_code == 429:
            logger.warning("Too Many Requests (ignored due to update interval < 15mn)")
        else:
            logger.warning(f"Unmanaged response ({response.status_code}): {response.text}")
        return False
