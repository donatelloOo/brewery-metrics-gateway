from abc import ABC, abstractmethod

from model.metric_data import MetricData


## Abstract definition of a forwarder
class Forwarder(ABC):

    @staticmethod
    @abstractmethod
    def send(config: dict, metric_data: MetricData) -> bool:
        pass
