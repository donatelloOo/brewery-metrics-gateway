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
class GrainfatherForwarder(Forwarder):

    @staticmethod
    def send(config: dict, metric_data: MetricData) -> bool:
        """
        Send metric data to Grainfather endpoint.

        Expected format is:
        {
            "specific_gravity": 1.034, // This must be a numeric value
            "temperature": 18, // This must be numeric
            "unit": "celsius" || "fahrenheit" // Supply the unit that matches the temperature you are sending
        }
        """
        url = config['serverUrl']
        data_to_send = {
            'specific_gravity': metric_data.gravity,
            'temperature': metric_data.temperature,
            'unit': 'celsius' if metric_data.temperature_unit == TemperatureUnit.CELSIUS else 'fahrenheit'
        }
        logger.debug("Sending data to Grainfather : %s , %s", url, data_to_send)
        response = requests.post(url, data_to_send, timeout=10)

        if response.status_code in (200,201):
            logger.info(f"Grainfather - Update Success: {response.text}")
            return True
        elif response.status_code == 422:
            logger.error(f"Grainfather - Invalid request: {response.text}")
        elif response.status_code == 429:
            logger.warning(f"Grainfather - Too Many Requests (ignored due to update interval < 15mn)")
        else:
            logger.warning(f"Grainfather - Unmanaged response ({response.status_code}): {response.text}")
        return False
