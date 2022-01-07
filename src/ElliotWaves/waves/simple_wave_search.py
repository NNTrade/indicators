from __future__ import annotations
import logging
from typing import List
import pandas as pd
from .simple_wave_builder import try_build_wave
from ..misc.direction import direction
from ..misc.wave import wave
from ..misc.candle_name import *

class search_wave:
    '''
    Поиск простой волны
    '''
    def __init__(self, wave_direction: direction) -> None:
        self.__dfFilter = DataFrameFilter(wave_direction)
        self.wave_direction = wave_direction
        self.logger = logging.getLogger("search_wave")
        self.double_filter = double_filter(wave_direction)
        pass

    def search(self, df: pd.DataFrame, next_dircetion_will_be_reversed: bool = False) -> List[wave]:
        """Ищем все возможные простые волны на данном интервале и с началом в начале интервале

        Args:
            df (pd.DataFrame): интервал поиска
            next_dircetion_will_be_reversed (bool, optional): Указатель, что следующая волна будет противоположно направлена. Defaults to False.

        Returns:
            List[wave]: список найденных волн
        """
        _ret = []
        self.logger.debug(
            f"Start search waves in DataFrame from {df.index[0]} till {df.index[-1]}")
        df_f = self.__dfFilter.filter(df)
        self.logger.debug(
            f"Filtered DataFrame from {df.index[0]} till {df.index[-1]}")
        for idx in df_f.index[::-1]:

            if next_dircetion_will_be_reversed:
                if not self.double_filter.check(df_f,idx):
                    continue

            self.logger.debug(
                f"Try build wave from {df_f.index[0]} till {idx}")
            res, resp = try_build_wave(
                df_f[df_f.index <= idx], self.wave_direction)
            if res:
                self.logger.debug(f"- SUCCESS")
                _ret.append(resp)
            else:
                self.logger.debug(f"- ERROR:")
                for err in resp:
                    self.logger.debug(f"-- {err}")
        return _ret

class DataFrameFilter:
    '''
    Фильтр DataFrame для поска волны
    Сужает область поска полны, отбрасывая области в которые волна точно не сможет попасть
    '''
    def __init__(self, wave_direction: direction) -> None:
        if wave_direction == direction.Long:
            self.high_label = High
            self.low_label = Low
            self.__right_border_search = self.__right_border__Long
        elif wave_direction == direction.Short:
            self.high_label = Low
            self.low_label = High
            self.__right_border_search = self.__right_border__Short
        else:
            raise Exception(f"unknown direction {wave_direction}")
        pass

    @staticmethod
    def getLongFilter() -> DataFrameFilter:
        return DataFrameFilter(direction.Long)

    @staticmethod
    def getShortFilter() -> DataFrameFilter:
        return DataFrameFilter(direction.Short)

    def __right_border__Long(self, df: pd.DataFrame):
        ## Если сделующая свеча противоположна направлена испомомму направлению, что вариантов нет
        if df.iloc[1][self.low_label] < df.iloc[0][self.low_label]:
            return pd.DataFrame(columns=df.columns)

        ## Ищем границу, на основе того, что волна не должна опускаться ниже старта
        df_filter_by_low = df[df[self.low_label] < df.iloc[0][self.low_label]]
        if len(df_filter_by_low) > 0:
            right_border_by_low = df_filter_by_low.iloc[0].name
            df_f: pd.DataFrame = df[df.index < right_border_by_low]
        else:
            df_f: pd.DataFrame = df

        ## Ищем максимум на имеющемся интервале, дальше него волна не может зайти
        max_idx_arr = df_f[df_f[self.high_label]
                           == df_f[self.high_label].max()].index
        if len(max_idx_arr) == 0:
            right_border_by_high = df_f[self.high_label].idxmax()
        else:
            right_border_by_high = max_idx_arr[-1]

        df_f = df_f[df_f.index <= right_border_by_high]
        return df_f

    def __right_border__Short(self, df: pd.DataFrame):        
        if df.iloc[1][self.low_label] > df.iloc[0][self.low_label]:
            return pd.DataFrame(columns=df.columns)

       
        df_filter_by_low = df[df[self.low_label] > df.iloc[0][self.low_label]]
        if len(df_filter_by_low) > 0:
            right_border_by_low = df_filter_by_low.iloc[0].name
            df_f: pd.DataFrame = df[df.index < right_border_by_low]
        else:
            df_f: pd.DataFrame = df

        min_idx_arr = df_f[df_f[self.high_label]
                           == df_f[self.high_label].min()].index
        if len(min_idx_arr) == 0:
            right_border_by_high = df_f[self.high_label].idxmin()
        else:
            right_border_by_high = min_idx_arr[-1]

        df_f = df_f[df_f.index <= right_border_by_high]
        return df_f

    def filter(self, df: pd.DataFrame) -> pd.DataFrame:
        if len(df.index) <= 1:
            return pd.DataFrame(columns=df.columns)
        return self.__right_border_search(df)


class double_filter:
    '''
    Проверяем, что последующее движение будет противоположным относительно текущего
    это позволяет исключить заведомо ложные волны, т.к. последующее движение будет продолжать текущую волну
    '''
    def __init__(self, wave_direction: direction) -> None:
        self.wave_direction = wave_direction
        self.logger = logging.getLogger("double_fliter")
        if wave_direction == direction.Long:
            self.high_label = High
            self.low_label = Low
            self.compare_func = self.__check_long__
        elif wave_direction == direction.Short:
            self.high_label = Low
            self.low_label = High
            self.compare_func = self.__check_short__
        else:
            raise Exception(f"unknown direction {wave_direction}")
        self.prev_idx = None
        pass

    def __check_long__(self, df: pd.DataFrame, idx) -> bool:
        if self.prev_idx is not None and df[self.high_label][self.prev_idx] > df[self.high_label][idx]:
            _ret = False
            self.logger.debug(
                f"Skip wave from {df.index[0]} till {idx}")
        else:
            _ret = True
        self.prev_idx = idx

        return _ret

    def __check_short__(self, df: pd.DataFrame, idx) -> bool:
        if self.prev_idx is not None and df[self.high_label][self.prev_idx] < df[self.high_label][idx]:
            _ret = False
            self.logger.debug(
                f"Skip wave from {df.index[0]} till {idx}")
        else:
            _ret = True
        self.prev_idx = idx

        return _ret

    def check(self, df: pd.DataFrame,idx):
        return self.compare_func(df,idx)


