from abc import ABC, abstractmethod
from pyspark.sql import DataFrame


class Blockchain(ABC):
    @abstractmethod
    def extract(self, mint_address: str):
        pass

    @abstractmethod
    def transform(self) -> DataFrame:
        pass

    @abstractmethod
    def load(self, df: DataFrame):
        pass

