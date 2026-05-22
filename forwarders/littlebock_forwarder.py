import requests
import logging
from model.forwarder import Forwarder
from model.metric_data import MetricData, TemperatureUnit


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('app.log'),  # log to file
        logging.StreamHandler()          # log to console
    ]
)
logger = logging.getLogger(__name__)

# Define the BrewCreator handler
class LittlebockForwarder(Forwarder):

    @staticmethod
    def send(config: dict, metric_data: MetricData) -> bool:
        """
        Send data to Littlebock endpoint.

        Expected format is:
        {
            "gravity": 1.034, // This must be a numeric value
            "temperature": 18, // This must be numeric
            "battery": "98" // This must be numeric
        }
        """
        url = config['serverUrl']
        data_to_send = {
            'gravity': metric_data.gravity,
            'temperature': metric_data.temperature,
            'battery': metric_data.battery,
        }
        logger.debug("Sending data to Littlebock : %s , %s", url, data_to_send)
        response = requests.post(url, data_to_send, timeout=10)

        if "not attached" in response.json()['message']:
            logger.warning("Littlebock - This device is not attached to a brew session")
            logger.debug(f"Littlebock - {response.json()}")
        else:
            logger.info("Littlebock - Update Success")
            return True
        return False
