from .tool.naming import Indicators, get_col_name
import numpy as np
import pandas as pd

class EmaBuilder(object):
    @staticmethod
    def BuildFor(value_sr: pd.Series, period:int, is_last:pd.Series=None ) -> pd.Series:
            return EmaBuilder(period).get_for(value_sr,is_last)

    def __init__(self, period):
        self.__a__ = 2 / (period + 1)
        self.__period = period

    def get_name_for(self, sr: pd.Series)->str:
        return get_col_name(Indicators.EMA, [str(self.__period)], [sr.name])
    
    def get_for(self, sr: pd.Series, is_last:pd.Series=None) -> pd.Series:
        """
        get Series with EMA by Values in Series
        sr - Series of Values
        is_last - optionol series of flags witch indicates that this value last in candle
                use it when you have values of one TimeFrame
                and you need EMA of TimeFrame Higher than you have

                Example: You have 10min values and you need EMA of 30min values
        """
        class worker:
            def __init__(self, a: float):
                self.__a__ = a
                self.__prev_ema__ = np.NaN

            def calc(self, value: float, is_last = True):
                if np.isnan(self.__prev_ema__):
                    cur_ema = value
                else:
                    cur_ema = self.__a__ * value + (1 - self.__a__) * self.__prev_ema__
                if is_last:
                    self.__prev_ema__ = cur_ema
                return cur_ema

        wrk = worker(self.__a__)

        if is_last is not None:
            ret_sr = pd.concat([sr, is_last], axis=1).apply(lambda row: wrk.calc(row.iloc[0], row.iloc[1]),axis=1)
        else:
            ret_sr = sr.apply(lambda val: wrk.calc(val))
        ret_sr = ret_sr.rename(self.get_name_for(sr))
        return ret_sr



class SmaBuilder(object):
    @staticmethod
    def BuildFor(value_sr: pd.Series, period:int, is_last:pd.Series=None ) -> pd.Series:
            return SmaBuilder(period).get_for(value_sr,is_last)

    def __init__(self, period):
        self.__period = period

    def get_name_for(self, sr: pd.Series)->str:
        return get_col_name(Indicators.SMA, [str(self.__period)], [sr.name])

    def get_for(self, sr: pd.Series, is_last:pd.Series=None) -> pd.Series:
        """
        get Series with EMA by Values in Series
        sr - Series of Values
        is_last - optionol series of flags witch indicates that this value last in candle
                use it when you have values of one TimeFrame
                and you need EMA of TimeFrame Higher than you have

                Example: You have 10min values and you need EMA of 30min values
        """
        

        wrk = SmaBuilder.Worker(self.__period)

        if is_last is not None:
            ret_sr = pd.concat([sr, is_last], axis=1).apply(lambda row: wrk.calc(row.iloc[0], row.iloc[1]),axis=1)
        else:
            ret_sr = sr.apply(lambda val: wrk.calc(val))
        ret_sr = ret_sr.rename(self.get_name_for(sr))
        return ret_sr
    
    class Worker:
        def __init__(self, period: float):
            self.__period = period
            self.__last_value_list =[]

        def calc(self, value: float, is_last = True)->float:
            last_val_count = len(self.__last_value_list)
            if last_val_count == self.__period:
                sum_v = np.sum(self.__last_value_list[1:]) + value
                ret_v = sum_v / last_val_count
            else:
                sum_v = np.sum(self.__last_value_list) + value
                ret_v = sum_v / (last_val_count + 1)

            if is_last:
                if last_val_count == self.__period:
                    self.__last_value_list.pop(0)
                self.__last_value_list.append(value)
            return ret_v