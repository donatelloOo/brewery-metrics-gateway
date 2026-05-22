from dataclasses import dataclass
from enum import Enum


class TemperatureUnit(Enum):
    CELSIUS = 'C'
    FAHRENHEIT = 'F'


@dataclass
class MetricData:
    # The specific gravity
    gravity: float  # | None

    # The temperature
    temperature: float  # | None

    # The temperature unit
    temperature_unit: TemperatureUnit  # | None

    # The battery percentage
    battery: float  # | None
