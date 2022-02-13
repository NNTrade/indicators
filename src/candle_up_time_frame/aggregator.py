from __future__ import annotations
import logging
from typing import Dict, List
import pandas as pd
from quote_source.client.TimeFrame import TimeFrame
from .builder import get_first_in_candle_flag, get_new_open_col,get_new_close_col,get_new_high_col,get_new_low_col,get_new_volume_col
from .dt_compare import compare_strategy
from .open_candle_dt import getOpenDTForSR
from .checks import check_tf_could_be_up, count_candle_in_up_candle

class ColMap:
    def __init__(self, open: str, close: str, high: str, low: str, volume: str):
        self.Open = open
        self.High = high
        self.Low = low
        self.Close = close
        self.Volume = volume

    @staticmethod
    def get_short_map() -> ColMap:
        return ColMap("O", "C", "H", "L", "V")

    @staticmethod
    def get_camelcase_map() -> ColMap:
        return ColMap("Open", "Close", "High", "Low", "Volume")

    @staticmethod
    def get_snake_case_map() -> ColMap:
        return ColMap("open", "close", "high", "low", "volume")

    @staticmethod
    def get_capscase_map() -> ColMap:
        return ColMap("OPEN", "CLOSE", "HIGH", "LOW", "VOLUME")


class Aggregator:
    """
    Объединяет данные свечей в TimeFrame более высокого порядка
    """
    def __init__(self, compare_dt_strategy=compare_strategy, col_map: ColMap = ColMap.get_short_map()) -> None:
        """Конструктор

        Args:
            compare_dt_strategy ([type], optional): Стратегия для получения функции определения начала новой свечи. Defaults to CompareStrategy.
            col_map (Condenser.colmap, optional): Маппер названий колонок и их назначение. Defaults to colmap.get_short_map().
        """
        self.logger = logging.getLogger("Condencer")
        self._comp_dt_str = compare_dt_strategy
        self._col_map = col_map

    @staticmethod
    def check_tf_could_be_converted(base_tf:TimeFrame, target_tf:TimeFrame):
        if check_tf_could_be_up(base_tf,target_tf) == False:
            raise Exception(f"Cann't convert data from TimeFrame {base_tf} to {target_tf}")
        
        if count_candle_in_up_candle(base_tf, target_tf) == False:
            raise Exception(f"TimeFrame {target_tf} not bigger than {base_tf}")
        
    def aggregate(self, df: pd.DataFrame, target_tf: TimeFrame, add_col_with_target_open_dt: bool = False) -> pd.DataFrame:
        """Объеденить данные

        Args:
            df (pd.DataFrame): базовые данные
            target_tf (TimeFrame): целевой timeframe
            add_col_with_target_open_dt (bool, optional): Добавить колонку с началом свечи более высокого порядка?. Defaults to False.

        Returns:
            pd.DataFrame: Результирующий DataFrame
        """
        flg_sr = get_first_in_candle_flag(
            df.index, self._comp_dt_str(target_tf))
        new_open = get_new_open_col(
            df[self._col_map.Open], flg_sr)
        new_high = get_new_high_col(
            df[self._col_map.High], flg_sr)
        new_low = get_new_low_col(df[self._col_map.Low], flg_sr)
        new_close = get_new_close_col(
            df[self._col_map.Close], flg_sr)
        new_volume = get_new_volume_col(
            df[self._col_map.Volume], flg_sr)
        ret_df = pd.DataFrame(
            [new_open, new_high, new_low, new_close, new_volume]).transpose()

        if add_col_with_target_open_dt:
            ret_df["DT"] = getOpenDTForSR(
                pd.Series(df.index, index=df.index, name="DT"), target_tf)

        return ret_df

    def aggregate_mass(self, df: pd.DataFrame, target_tf_list: List[TimeFrame], add_col_with_target_open_dt: bool = False) -> Dict[TimeFrame, pd.DataFrame]:
        return dict((tf, self.aggregate(df, tf, add_col_with_target_open_dt)) for tf in target_tf_list)
