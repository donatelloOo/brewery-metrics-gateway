from abc import ABC, abstractmethod

from model.metric_data import MetricData


## Abstract definition of a handler
class Handler(ABC):

    @staticmethod
    @abstractmethod
    def transform(config: dict, data: dict) -> MetricData:
        pass
