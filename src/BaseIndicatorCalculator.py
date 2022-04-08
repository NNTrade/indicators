from abc import ABC, abstractmethod
from typing import Dict, Tuple
import pandas as pd

class BaseIndicatorCalculator(ABC):
  def __init__(self, config:Dict = {}) -> None:
    self.__config = config

  @property
  def config(self) ->Dict:
    return self.__config
  
  @abstractmethod
  def calc_value(self,candle: pd.Series, state:Dict) -> Tuple[Dict[str,float], Dict]:
    """Calculate indicator

    Args:
        candle (pd.Series): currenct series of values
        state (float): state of calculation        

    Returns:
        Tuple[Dict[str, float], Dict]: tuple of indicator values and new state of indicator
    """
    ...