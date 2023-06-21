from abc import ABC, abstractmethod


class Currency(ABC):
    @abstractmethod
    def extract(self, param):
        pass

    @abstractmethod
    def transform(self, param):
        pass

    def load(self, param):
        pass
