from abc import ABC, abstractmethod

from model.config import Config
from model.metric import MetricData


# Abstract definition of a handler
class Handler(ABC):

    @staticmethod
    @abstractmethod
    def transform(config: Config.HandlerConfig, data: dict) -> MetricData:
        pass
