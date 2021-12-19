from .point import point
from .type import type
import pandas as pd

class wave:
    def __init__(self, start: point, end: point) -> None:
        self.__start = start
        self.__end = end
        self.__height = abs(self.end - self.start)
        self.__time = self.end.timestamp - self.start.timestamp
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
        return type.not_implemented