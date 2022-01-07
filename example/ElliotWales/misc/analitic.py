from __future__ import annotations
import pandas as pd
from typing import List
from src.ElliotWaves.misc.wave import wave
from src.ElliotWaves.misc.direction import direction
from src.ElliotWaves.waves.impulse_five_search import condens_sub_waves
from src.RelativePercent.Factory import get_percent
        
def analitic_df(waves:List[wave])->pd.DataFrame:
    dir_col_name = "Direction"
    sub_waves_arr_col_name = "SubWaves"
    ret_waves_df =pd.DataFrame(pd.Series(condens_sub_waves(waves),name=sub_waves_arr_col_name))
    ret_waves_df["SubWaveCount"] = ret_waves_df[sub_waves_arr_col_name].map(lambda el: len(el))
    ret_waves_df[dir_col_name] = ret_waves_df[sub_waves_arr_col_name].map(lambda el: el[0].direction)
    ret_waves_df["Full"] = ret_waves_df["SubWaveCount"] == 5
    for idx in range(5):
        change_col_name = f"Wave{idx+1} Change%"
        waves_sr:pd.Series = ret_waves_df[ret_waves_df["SubWaveCount"] >= (idx+1)][sub_waves_arr_col_name]
        wave_sr:pd.Series = waves_sr.map(lambda el: el[idx])
        
        ret_waves_df[change_col_name] = get_percent(sr1=wave_sr.map(lambda el: el.end.price),sr2=wave_sr.map(lambda el: el.start.price))
        
        profit_col_name = f"Wave{idx+1} Profit%"
        ret_waves_df[profit_col_name] = ret_waves_df[change_col_name] * wave_sr.map(lambda el: (-1 if el.direction == direction.Short else 1 ))
    return ret_waves_df
