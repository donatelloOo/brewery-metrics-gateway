from abc import ABC, abstractmethod

from model.config import Config
from model.metric import MetricData


# Abstract definition of a forwarder
class Forwarder(ABC):

    @staticmethod
    @abstractmethod
    def send(config: Config.ForwarderConfig, metric_data: MetricData) -> bool:
        pass
