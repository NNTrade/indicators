from numpy import NaN
from src.ElliotWaves.direction import direction
import pandas as pd


class search:
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
    
    def __right_border__Long(self,df:pd.DataFrame):
        if df.iloc[1][self.low_label] < df.iloc[0][self.low_label]:
            return NaN

        right_border_by_low = df[df[self.low_label] < df.iloc[0][self.low_label]].iloc[0].name
        df_f:pd.DataFrame = df[df.index < right_border_by_low]

        right_border_by_high = df_f[self.high_label].idxmax()
        df_f = df_f[df_f.index <= right_border_by_high]
        return df_f  

    def __right_border__Short(self,df:pd.DataFrame):
        if df.iloc[1][self.low_label] > df.iloc[0][self.low_label]:
            return NaN

        right_border_by_low = df[df[self.low_label] > df.iloc[0][self.low_label]].iloc[0].name
        df_f:pd.DataFrame = df[df.index < right_border_by_low]

        right_border_by_high = df_f[self.high_label].idxmin()
        df_f = df_f[df_f.index <= right_border_by_high]  
        return df_f  

    def search_impulse_wave(self, df:pd.DataFrame):
        return self.__right_border_search(df)