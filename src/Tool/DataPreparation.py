import pandas as pd
import numpy as np
from typing import Tuple

def normilize(sr: pd.Series)->pd.Series:
    return (sr - sr.min())/(sr.max() - sr.min())
    
def log_tr(sr: pd.Series)->pd.Series:
    return (sr - sr.min() + 1).transform(np.log)

class handle_outlier:
    def __init__(self, factor:int = 3) -> None:
        self.factor = factor
        pass

    def __get_lim__(self,sr:pd.Series)->Tuple[float, float]:
        upper_lim = sr.mean () + sr.std () * self.factor  
        lower_lim = sr.mean () - sr.std () * self.factor  
        return lower_lim, upper_lim
    
    def find(self,sr:pd.Series)->pd.Series:
        lower_lim, upper_lim = self.__get_lim__(sr) 
        return sr.loc[(sr < lower_lim) & (sr > upper_lim)]

    def replace(self,sr:pd.Series)->pd.Series:
        lower_lim, upper_lim = self.__get_lim__(sr) 
        sr.loc[(sr > upper_lim)] = upper_lim
        sr.loc[(sr < lower_lim)] = lower_lim
        return sr