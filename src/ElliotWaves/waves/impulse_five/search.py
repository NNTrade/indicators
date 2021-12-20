from __future__ import annotations
from typing import List
from numpy import NaN, isnan
import pandas as pd
from ...direction import direction
from ...wave import wave
from .builder import builder_impulse_five
from .builder_correction_wave import try_build_wave as try_cor_build_wave
from .builder_impulse_wave import try_build_wave as try_imp_build_wave

class DataFrameFilter:
    def __init__(self,impulse_direction:direction) -> None:
        if impulse_direction == direction.Long:
            self.high_label = "H"
            self.low_label = "L"
            self.__right_border_search = self.__right_border__Long 
        elif impulse_direction == direction.Short:
            self.high_label = "L"
            self.low_label = "H"
            self.__right_border_search = self.__right_border__Short 
        else:
            raise Exception(f"unknown direction {impulse_direction}")
        pass
    
    @staticmethod
    def getLongFilter()->DataFrameFilter:
        return DataFrameFilter(direction.Long)

    @staticmethod
    def getShortFilter()->DataFrameFilter:
        return DataFrameFilter(direction.Short)

    def __right_border__Long(self,df:pd.DataFrame):
        if df.iloc[1][self.low_label] < df.iloc[0][self.low_label]:
            return NaN

        df_filter_by_low = df[df[self.low_label] < df.iloc[0][self.low_label]]
        if len(df_filter_by_low) > 0:
            right_border_by_low = df_filter_by_low.iloc[0].name
            df_f:pd.DataFrame = df[df.index < right_border_by_low]
        else:
            df_f:pd.DataFrame = df

        max_idx_arr = df_f[df_f[self.high_label] == df_f[self.high_label].max()].index
        if len(max_idx_arr) == 0:
            right_border_by_high = df_f[self.high_label].idxmax()
        else:
            right_border_by_high = max_idx_arr[-1]

        df_f = df_f[df_f.index <= right_border_by_high]
        return df_f  

    def __right_border__Short(self,df:pd.DataFrame):
        if df.iloc[1][self.low_label] > df.iloc[0][self.low_label]:
            return NaN

        df_filter_by_low = df[df[self.low_label] > df.iloc[0][self.low_label]]
        if len(df_filter_by_low) > 0:
            right_border_by_low = df_filter_by_low.iloc[0].name
            df_f:pd.DataFrame = df[df.index < right_border_by_low]
        else:
            df_f:pd.DataFrame = df

        min_idx_arr = df_f[df_f[self.high_label] == df_f[self.high_label].min()].index
        if len(min_idx_arr) == 0:
            right_border_by_high = df_f[self.high_label].idxmin()
        else:
            right_border_by_high = min_idx_arr[-1]

        df_f = df_f[df_f.index <= right_border_by_high]  
        return df_f  

    def filter(self, df:pd.DataFrame)->pd.DataFrame:
        return self.__right_border_search(df)

class search_wave:
    def __init__(self,impulse_direction:direction) -> None:
        self.__dfFilter = DataFrameFilter(impulse_direction)
        if impulse_direction == direction.Long:
            self.builder = 

    def search(self, df:pd.DataFrame)->List[wave]:
        df_f = self.__dfFilter.filter(df)
        
        


class search_impulse_five:
    def __init__(self,impulse_direction:direction) -> None:
        self.search_impulse = search_wave(impulse_direction)
        self.search_correction = search_wave(impulse_direction.revers())
    
    def search(self, df:pd.DataFrame):
        builer_imp_five = builder_impulse_five()
        

