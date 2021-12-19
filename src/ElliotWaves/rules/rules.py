import pandas as pd

from ..direction import direction
from ..wave import wave

from typing import List

def __direction_adapter__(base_compare: bool, direction: direction)-> bool:
    if direction == direction.Long: return base_compare
    if direction == direction.Short: return not base_compare
    raise Exception(f"unknown direction {direction}")

def ex_check(name:str, function_return:bool):
    if not function_return:
        raise Exception(f"{name}: FAIL")

def EW2_gt_SW1(wave1: wave, wave2: wave, direction: direction)->bool:
    if  wave2.end.price == wave1.start.price:
        return False
    ret = wave2.end.price > wave1.start.price
    return __direction_adapter__(ret, direction)

def EW3_gt_EW1(wave1: wave, wave3: wave, direction: direction)->bool:
    if  wave3.end.price == wave1.end.price:
        return False
    ret = wave3.end.price > wave1.end.price
    return __direction_adapter__(ret, direction)

def HW3_gt_HW1_or_HW3_gt_HW5(wave1:wave, wave3:wave, wave5:wave)->bool:
    return wave3.height > wave1.height or wave3.height > wave5.height

def EW5_gt_EW3(wave3: wave, wave5: wave, direction: direction)->bool:
    if wave5.end.price == wave3.end.price:
        return False
    ret = wave5.end.price > wave3.end.price
    return __direction_adapter__(ret, direction)

def W2_dif_W4(wave2: wave, wave4: wave)->bool:
    return wave2.height != wave4.height or wave2.time != wave4.time or wave2.type != wave4.type

def HWx_gt_HWy_and_HWx_gt_HWz(waves1:wave, wave3:wave, wave5:wave, power:float)->bool:
    '''
    power = HWx/HWy - 1
    '''
    heights = [waves1.height,wave3.height,wave5.height]
    heights.sort(reverse=True)
    return heights[0]/heights[1] - 1 > power

def __timedelta_to_second(td:pd.Timedelta)->int:
    return td.days*24*60*60 + td.seconds
    
def TWx_not_TWy_not_TWz(waves:List[wave], dif_percent: float)->bool:
    '''
    dif_percent = TWx/TWy - 1
    '''
    if len(waves) != 3:
        raise Exception(f"wrong wave count")
    
    times = [wave.time for wave in waves]
    times.sort(reverse=True)
    return (__timedelta_to_second(times[0])/__timedelta_to_second(times[1]) - 1) > dif_percent
    
def EWx_SWx_is_ext_RWx(wave: wave, df:pd.DataFrame, wave_direction:direction)->bool:
    if wave_direction == wave_direction.Long:
        return (wave.end.price >= max(df["H"])) and (wave.start.price <= min(df["L"]))
    elif wave_direction == wave_direction.Short:
        return (wave.end.price <= min(df["L"])) and (wave.start.price >= max(df["H"]))
