import pandas as pd
from .tool.naming import get_col_name, Indicators
from .ma import SmaBuilder

class SmaGainBuilder(object):
    @staticmethod
    def BuildFor(value_sr: pd.Series, period:int, is_last:pd.Series=None ) -> pd.Series:
            return SmaGainBuilder(period).get_for(value_sr,is_last)

    def __init__(self, period):
        self.__period = period

    def get_name_for(self, sr: pd.Series)->str:
        return get_col_name(Indicators.SMAGain, [str(self.__period)], [sr.name])

    def get_for(self, sr: pd.Series, is_last:pd.Series=None) -> pd.Series:
        """
        get Series with EMA by Values in Series
        sr - Series of Values
        is_last - optionol series of flags witch indicates that this value last in candle
                use it when you have values of one TimeFrame
                and you need EMA of TimeFrame Higher than you have

                Example: You have 10min values and you need EMA of 30min values
        """
    
        wrk = SmaGainBuilder.Worker(self.__period)

        if is_last is not None:
            ret_sr = pd.concat([sr, is_last], axis=1).apply(lambda row: wrk.calc(row.iloc[0], row.iloc[1]),axis=1)
        else:
            ret_sr = sr.apply(lambda val: wrk.calc(val))
        ret_sr = ret_sr.rename(self.get_name_for(sr))
        return ret_sr
    
    class Worker:
        def __init__(self, period: float):
            self.__ma_worker = SmaBuilder.Worker(period)
            self.__prev_val = None

        def _calc_delta(self, value: float, is_last = True)->float|None:
            if self.__prev_val is not None:
                ret_delta = value - self.__prev_val
            else:
                ret_delta = None
        
            if is_last:
                self.__prev_val = value
        
            return ret_delta
        
        def calc(self, value: float, is_last = True)->float|None:         
            delta = self._calc_delta(value, is_last)
            
            if delta is None:
                return None
            elif delta < 0:
                delta = 0
                        
            return self.__ma_worker.calc(delta, is_last)
        

class SmaLossBuilder(object):
    @staticmethod
    def BuildFor(value_sr: pd.Series, period:int, is_last:pd.Series=None ) -> pd.Series:
            return SmaLossBuilder(period).get_for(value_sr,is_last)

    def __init__(self, period):
        self.__period = period

    def get_name_for(self, sr: pd.Series)->str:
        return get_col_name(Indicators.SMALoss, [str(self.__period)], [sr.name])

    def get_for(self, sr: pd.Series, is_last:pd.Series=None) -> pd.Series:
        """
        get Series with EMA by Values in Series
        sr - Series of Values
        is_last - optionol series of flags witch indicates that this value last in candle
                use it when you have values of one TimeFrame
                and you need EMA of TimeFrame Higher than you have

                Example: You have 10min values and you need EMA of 30min values
        """
    
        wrk = SmaLossBuilder.Worker(self.__period)

        if is_last is not None:
            ret_sr = pd.concat([sr, is_last], axis=1).apply(lambda row: wrk.calc(row.iloc[0], row.iloc[1]),axis=1)
        else:
            ret_sr = sr.apply(lambda val: wrk.calc(val))
        ret_sr = ret_sr.rename(self.get_name_for(sr))
        return ret_sr
    
    class Worker:
        def __init__(self, period: float):
            self.__ma_worker = SmaBuilder.Worker(period)
            self.__prev_val = None

        def _calc_delta(self, value: float, is_last = True)->float|None:
            if self.__prev_val is not None:
                ret_delta = value - self.__prev_val
            else:
                ret_delta = None
        
            if is_last:
                self.__prev_val = value
        
            return ret_delta
        
        def calc(self, value: float, is_last = True)->float|None:
            delta = self._calc_delta(value, is_last)
            
            if delta is None:
                return None
            elif delta > 0:
                delta = 0
            
            delta = abs(delta)

            return self.__ma_worker.calc(delta, is_last)
