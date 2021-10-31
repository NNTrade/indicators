import numpy as np
import pandas as pd
import logging

class EmaBuilder(object):
    def __init__(self, period):
        self.__a__ = 2 / (period + 1)
        self.Name = f'EMA{period}'
        self.logger = logging.getLogger(f"EmaCalculator[{self.Name}]")

    def expect_name(self, of_field: str) -> str:
        return f'{self.Name}[{of_field}]'

    def getSr(self, sr: pd.Series, is_last:pd.Series=None) -> pd.Series:
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

        if type(sr.name) is tuple:
            cur_name = sr.name[:-1] + (self.expect_name(sr.name[-1]),)
        else:
            cur_name = self.expect_name(sr.name)

        wrk = worker(self.__a__)

        if is_last is not None:
            ret_sr = pd.concat([sr, is_last], axis=1).apply(lambda row: wrk.calc(row.iloc[0], row.iloc[1]),axis=1)
        else:
            ret_sr = sr.apply(lambda val: wrk.calc(val))
        ret_sr = ret_sr.rename(cur_name)
        return ret_sr

    def getDf(self, df: pd.DataFrame, df_of_flags: pd.DataFrame=None)->pd.DataFrame:
        """
        get DataFrame with EMA by Values in DataFrame
        df - DataFrame of Values
        df_of_flags - optional DataFrame of flags witch indicates that this value last in candle
                        use it when you have values of one TimeFrame
                        and you need EMA of TimeFrame Higher than you have

                        Name of columns must be equals of names of columns in df

                        Example: You have 10min values and you need EMA of 30min values
        """
        _return = []
        for label, content in df.items():
            self.logger.log(level=logging.INFO, msg=f'Add {self.Name} to col {label}')
            if df_of_flags is not None:
                _return.append(self.getSr(content), df_of_flags[label])
            else:
                _return.append(self.getSr(content))
        return pd.concat(_return, axis=1)

def Create(value_sr: pd.Series, period:int, is_last:pd.Series=None ) -> pd.Series:
    return EmaBuilder(period).getSr(value_sr,is_last)