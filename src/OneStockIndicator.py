from abc import ABC
from typing import Dict
import pandas as pd
from .Tool.ColName import OpenCandleDT as Odt
from .BaseIndicatorCalculator import BaseIndicatorCalculator

class OneStockIndicator(ABC):
  def __init__(self, ind_calc:BaseIndicatorCalculator) -> None:
    self._state:Dict = {}
    self._prev_state:Dict = {}
    self._ind_calc = ind_calc
    self._prevOdt = None

  def get_state(self)-> Dict:
    return self._state.copy()
      
  def get_next(self, series: pd.Series)->Dict[str, float]:
    """Get Next indicator value

    Args:
        series (pd.Series): currenct series

    Returns:
        Dict[str, float]: New indicator values
    """
        
    if (series[Odt] == self._prevOdt):
      self._state = self._prev_state
    else:
      self._prevOdt = series[Odt]
    
    new_value, new_state = self._ind_calc.calc_value(series, self.get_state())
    
    self._prev_state = self._state
    self._state = new_state
    
    return new_value
    

      
  