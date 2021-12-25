from numpy import NaN
from .direction import direction
from .point import point
from .type import type
import pandas as pd

class wave:
    def __init__(self, start: point, end: point, type: type = type.not_implemented) -> None:
        self.__start:point = start
        self.__end:point = end
        self.__height:float = abs(self.end.price - self.start.price)
        self.__time:pd.Timedelta = self.end.timestamp - self.start.timestamp
        self.__time_in_sec:int = self.__time.days*24*60*60 + self.__time.seconds
        self.__type:type = type
        if self.__end.price > self.__start.price:
            self.__direction = direction.Long
        elif self.__end.price < self.__start.price:
            self.__direction = direction.Short
        else:
            self.__direction = NaN
        pass
    
    @property
    def start(self) -> point:
        return self.__start

    @property
    def end(self) -> point:
        return self.__end
    
    @property
    def height(self) -> float:
        return self.__height
    
    @property
    def time(self) -> pd.Timedelta:
        return self.__time
    
    @property
    def type(self) -> type:
        return self.__type

    @property
    def time_is_sec(self) -> int:
        return self.__time_in_sec

    @property
    def direction(self) -> direction:
        return self.__direction
    
    def __str__(self) -> str:
        return f"From: {self.__start} Till: {self.__end} Direction: {self.__direction}"