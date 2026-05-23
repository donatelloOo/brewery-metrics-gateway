import logging
from model.handler import Handler
from model.metric_data import MetricData, TemperatureUnit

# Logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('app.log'),  # log to file
        logging.StreamHandler()  # log to console
    ]
)
logger = logging.getLogger(__name__)


# Define the BrewCreator handler
class BrewCreatorHandler(Handler):

    @staticmethod
    def transform(config: dict, data: dict) -> MetricData:
        """
        Receives BrewCreator POST requests.
        
        Expected format is:
        {
            'name': '<deviceName>',
            'temp': 18.3,
            'temp_unit': 'C',
            'gravity': 1.009
        }
        """
        return MetricData(
            gravity=data.get('gravity'),
            temperature=data.get('temp'),
            temperature_unit=TemperatureUnit.CELSIUS if data.get('temp_unit') == 'C'
            else TemperatureUnit.FAHRENHEIT,
            battery=None,
            device_name=data.get('name'))
