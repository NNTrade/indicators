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

def change_col_name(df:pd.DataFrame):
    arr = []
    for col in df.columns:
        if "Profit%" in col :
            arr.append(["Profit %",col[0:5]])
        elif "Change%" in col :
            arr.append(["Change %",col[0:5]])
        else:
            arr.append([col,"Waves"])
    _ret = df.copy()
    _ret.columns = pd.MultiIndex.from_frame(pd.DataFrame(arr,columns=["Type", "Wave"]))
    return _ret

def wave_close_df(df:pd.DataFrame, close_count:int):
    df_n_plus = df[df[("Count","Waves")]>=close_count]
    ret_df = pd.DataFrame(data={"value_done":df_n_plus[("Profit %", f"Wave{close_count}")],"value":df_n_plus[("Profit %", f"Wave{close_count+1}")],"dir":df_n_plus[("Direction", f"Waves")],"full":df_n_plus[("Count","Waves")]==5})
    ret_df["count"] = close_count
    return ret_df

def get_statistic(df:pd.DataFrame)->pd.DataFrame:
    sns_df = pd.DataFrame(columns=["value_done","value","dir","full","count"])
    for close_count in [1,2,3,4]:
        sns_df = sns_df.append(wave_close_df(df, close_count))
    sns_df["value"] = sns_df["value"].fillna(-1)
    return sns_df