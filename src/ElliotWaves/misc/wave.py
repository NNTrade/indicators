from __future__ import annotations
from numpy import NaN
from .direction import direction
from .point import point
from .type import type
import pandas as pd
from typing import List

class wave:
    def __init__(self, start: point, end: point, type: type = type.not_implemented, sub_waves: List[wave] = []) -> None:
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
            self.__direction = None
        
        if len(sub_waves) > 0:
            for idx in range(len(sub_waves)-1):
                if not sub_waves[idx].isLinkedNext(sub_waves[idx+1]):
                    raise Exception(f"Sub waves is unlinked")
            if not sub_waves[0].start.isEqual(self.__start):
                raise Exception(f"Sub waves should be started from the start of upper wave")
            if not sub_waves[-1].end.isEqual(self.__end):
                raise Exception(f"Sub waves should be ended from the end of upper wave")
            if len(sub_waves) == 1:
                raise Exception("Sub waves count couldn't be 1")
            
        self.__sub_waves = sub_waves
        pass
    
    @property
    def sub_waves(self)-> List[wave]:
        return [wv for wv in self.__sub_waves]
    
    @property
    def sub_wave_count(self)->int:
        return len(self.__sub_waves)
    
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
    
    def isLinkedNext(self, next_wave:wave)->bool:
        return self.end.isEqual(next_wave.start)