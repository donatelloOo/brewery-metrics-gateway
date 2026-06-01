import logging

from model.config import Config
from model.handler import Handler
from model.metric import MetricData, TemperatureUnit

# Logger
logger = logging.getLogger(__name__)


# Define the BrewCreator handler
class BrewCreatorHandler(Handler):

    @staticmethod
    def transform(config: Config.HandlerConfig, data: dict) -> MetricData:
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
