from typing import Dict, Tuple
import pandas as pd
from ..BaseIndicatorCalculator import BaseIndicatorCalculator
from ..Tool.ColName import Close as C

class ValueFactory(BaseIndicatorCalculator):
  def __init__(self, period: int, strict: bool = False, value_col_name: str = C) -> None:
      super().__init__({"period": period, "strict": strict, "value": value_col_name})
  
  def calc_value(self, candle: pd.Series, state: Dict) -> Tuple[Dict[str, float], Dict]:
      candle_value = candle[self.config["value"]]
      period = self.config["period"]
      if (len(state) == 0):
        new_lenght = 1
        cur_value = candle_value
      else:
        state_len = state["lenght"]
        if (state_len < period):
          new_lenght = state_len + 1
        else:
          new_lenght = period
        cur_value =  (state["prev"] * (new_lenght - 1) + candle_value) / new_lenght
        
      state["lenght"] = new_lenght
      state["prev"] = cur_value
      cur_value
      if self.config["strict"]:
        if (new_lenght < period):
          cur_value = None
      return {"SMA": cur_value}, state