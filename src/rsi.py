import pandas as pd
from .tool.naming import Indicators
from .gain_loss import SmaGainBuilder, SmaLossBuilder, baseSingleSourceBuilder

class RSBuilder(baseSingleSourceBuilder):
    @staticmethod
    def BuildFor(value_sr: pd.Series, period:int, is_last:pd.Series=None ) -> pd.Series:
            return RSBuilder(period).get_for(value_sr,is_last)

    def __init__(self, period):
        self.__period = period
        super().__init__([str(period)])
    
    @property
    def get_indicator_id(self)->Indicators:
        return Indicators.RS
    
    def _get_for(self, sr: pd.Series, is_last:pd.Series=None, indicators_df:pd.DataFrame = None) -> pd.Series:
        gain_sr = self._get_gain(sr, is_last, indicators_df)
        loss_sr = self._get_loss(sr,is_last, indicators_df)
        ret_sr = gain_sr / loss_sr 
        ret_sr = ret_sr.rename(self.get_name_for(sr))
        return ret_sr

    def _get_gain(self, sr: pd.Series, is_last:pd.Series=None, indicators_df:pd.DataFrame = None) -> pd.Series:
        gain_builder = SmaGainBuilder(self.__period)
        gain_sr_name = gain_builder.get_name_for(sr)
        if indicators_df is not None and gain_sr_name in indicators_df.columns:
            gain_sr = indicators_df[gain_sr_name]
        else:
            gain_sr = gain_builder.get_for(sr, is_last)
        return gain_sr

    def _get_loss(self, sr: pd.Series, is_last:pd.Series=None, indicators_df:pd.DataFrame = None) -> pd.Series:
        loss_builder = SmaLossBuilder(self.__period)
        gain_sr_name = loss_builder.get_name_for(sr)
        if indicators_df is not None and gain_sr_name in indicators_df.columns:
            loss_sr = indicators_df[gain_sr_name]
        else:
            loss_sr = loss_builder.get_for(sr, is_last)
        return loss_sr
         
class RSIBuilder(baseSingleSourceBuilder):
    @staticmethod
    def BuildFor(value_sr: pd.Series, period:int, is_last:pd.Series=None ) -> pd.Series:
            return RSIBuilder(period).get_for(value_sr,is_last)

    def __init__(self, period):
        self.__period = period
        super().__init__([str(period)])
    
    @property
    def get_indicator_id(self)->Indicators:
        return Indicators.RSI
    
    def _get_for(self, sr: pd.Series, is_last:pd.Series=None, indicators_df:pd.DataFrame = None) -> pd.Series:
        rs_sr = self._get_rs(sr,is_last, indicators_df)
        ret_sr = 100 - 100 / (rs_sr+1)
        ret_sr = ret_sr.rename(self.get_name_for(sr))
        return ret_sr
    
    def _get_rs(self, sr: pd.Series, is_last:pd.Series=None, indicators_df:pd.DataFrame = None) -> pd.Series:
        rs_builder:RSBuilder = RSBuilder(self.__period)
        rs_sr_name = rs_builder.get_name_for(sr)
        if indicators_df is not None and rs_sr_name in indicators_df.columns:
            rs_sr = indicators_df[rs_sr_name]
        else:
            rs_sr = rs_builder.get_for(sr, is_last)
        return rs_sr