from __future__ import annotations
import pandas as pd

class point:
    def __init__(self, timestamp: pd.Timestamp, price:float) -> None:
        self.__timestamp = timestamp
        self.__price = price
        pass
    
    @property
    def timestamp(self) -> pd.Timestamp:
        return self.__timestamp

    @property
    def price(self) -> float:
        return self.__price
    
    def isEqual(self, point:point):
        return self.timestamp == point.timestamp and self.price == point.price
    
    def __str__(self) -> str:
       return f"TS:{self.__timestamp}, Value:{self.price}"