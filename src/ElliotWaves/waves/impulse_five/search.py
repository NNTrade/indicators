import pandas as pd

from src.ElliotWaves.direction import direction
def search_impulse_wave(df:pd.DataFrame, impulse_direction:direction):
    if impulse_direction == direction.Long:
        high_label = "H"
        low_label = "L"
    elif impulse_direction == direction.Short:
        high_label = "L"
        low_label = "H"
    else:
        raise Exception(f"unknown direction {impulse_direction}")
    
    #todo bug не < используется только при движении вверх
    if df.iloc[1][low_label] < df.iloc[0][low_label]:
        return #??
    right_border_by_low = df[df[low_label] < df.iloc[0][low_label]].iloc[0].name
    df_f:pd.DataFrame = df[df.index < right_border_by_low]
    
    right_border_by_high = df_f[high_label].idxmax()
    df_f = df_f[df_f.index <= right_border_by_high]

