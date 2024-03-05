from abc import ABC, abstractproperty, abstractmethod
from .indicator_list import Indicators
from .tool.naming import get_col_name
from typing import List
import pandas as pd

class baseBuilder(ABC):
    def __init__(self, parameters:List[str]) -> None:
        super().__init__()
        self.__parameters = parameters

    def get_name(self, series_names: List[str]|str)->str:
        if not isinstance(series_names, list):
            series_names = [series_names]
        return get_col_name(self.get_indicator_id, self.__parameters, series_names)
    
    def get_name_for(self, serieses: List[pd.Series]|pd.Series)->str:
        if not isinstance(serieses, list):
            serieses = [serieses]
        return self.get_name([s.name for s in serieses])
    
    @abstractproperty
    @property
    def get_indicator_id(self)->Indicators:
        ...
    
    @abstractmethod
    def get_for(self, serieses: List[pd.Series]|pd.Series, is_last:pd.Series=None, indicators_df:pd.DataFrame = None) -> pd.Series:
        ...

class baseSingleSourceBuilder(baseBuilder):
    def __init__(self, parameters:List[str]) -> None:
        super().__init__(parameters)    
    
    def get_for(self, serieses: List[pd.Series]|pd.Series, is_last:pd.Series=None, indicators_df:pd.DataFrame = None) -> pd.Series:
        assert isinstance(serieses, list) == False
        return self._get_for(serieses, is_last, indicators_df)
    
    @abstractmethod
    def _get_for(self, sr: pd.Series, is_last:pd.Series=None, indicators_df:pd.DataFrame = None) -> pd.Series:
        ...