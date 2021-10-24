from typing import List,Dict
from .Builder import EmaBuilder
import pandas as pd

class EmaFactory:
    def __init__(self, periods:List[int]) -> None:
        
        self.__emas__:Dict[int,EmaBuilder] = {}
        for p in periods:
            self.__emas__[p] = EmaBuilder(p)        
        pass

    @property
    def periods(self)->List[int]:
        return list(self.__emas__.keys())

    def getEma(self,col_sr:pd.Series, is_last:pd.Series=None)->pd.DataFrame:
        concat_arr = [ema_inst.getSr(col_sr, is_last) for ema_inst in self.__emas__.values()]
        return pd.concat(concat_arr, axis=1)