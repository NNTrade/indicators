import pandas as pd

from src.ElliotWaves.misc.candle_name import High, Low

from ..misc.direction import direction
from ..misc.wave import wave

from typing import List, Tuple

def __direction_adapter__(base_compare: bool, impulse_direction: direction)-> bool:
    if impulse_direction == impulse_direction.Long: return base_compare
    if impulse_direction == impulse_direction.Short: return not base_compare
    raise Exception(f"unknown direction {impulse_direction}")

def ex_check(name:str, function_return:bool):
    if not function_return:
        raise Exception(f"{name}: FAIL")

def EW2_gt_SW1(wave1: wave, wave2: wave, impulse_direction: direction)->bool:
    if  wave2.end.price == wave1.start.price:
        return False
    ret = wave2.end.price > wave1.start.price
    return __direction_adapter__(ret, impulse_direction)

def EW3_gt_EW1(wave1: wave, wave3: wave, impulse_direction: direction)->bool:
    if  wave3.end.price == wave1.end.price:
        return False
    ret = wave3.end.price > wave1.end.price
    return __direction_adapter__(ret, impulse_direction)

def HW3_gt_HW1_or_HW3_gt_HW5(wave1:wave, wave3:wave, wave5:wave)->bool:
    return wave3.height > wave1.height or wave3.height > wave5.height

def EW4_gt_EW1(wave1: wave, wave4: wave, impulse_direction: direction)->bool:
    if wave1.end.price == wave4.end.price:
        return False
    ret = wave4.end.price > wave1.end.price
    return __direction_adapter__(ret, impulse_direction)

def EW5_gt_EW3(wave3: wave, wave5: wave, impulse_direction: direction)->bool:
    if wave5.end.price == wave3.end.price:
        return False
    ret = wave5.end.price > wave3.end.price
    return __direction_adapter__(ret, impulse_direction)

def W2_dif_W4(wave2: wave, wave4: wave)->bool:
    return wave2.height != wave4.height or wave2.time_is_sec != wave4.time_is_sec or wave2.type != wave4.type

def HWx_gt_HWy_and_HWx_gt_HWz(waves1:wave, wave3:wave, wave5:wave, dif_percent:float = 0.2)->bool:
    '''
    power = HWx/HWy - 1
    '''
    heights = [waves1.height,wave3.height,wave5.height]
    heights.sort(reverse=True)
    return heights[0]/heights[1] - 1 > dif_percent
    
def TWx_not_TWy_not_TWz(waves:List[wave], dif_percent: float = 0.2)->bool:
    '''
    dif_percent = TWx/TWy - 1
    '''
    if len(waves) != 3:
        raise Exception(f"wrong wave count")
    
    times = [wave.time_is_sec for wave in waves]
    times.sort(reverse=True)
    
    for idx,time1 in enumerate(times):
        for time2 in times[idx+1:]:
            if (time1/time2 - 1) < dif_percent:
                return False
    return True
    
def EWx_SWx_is_ext_RWx(wave: wave, df:pd.DataFrame)->bool:
    if wave.direction == direction.Long:
        return (wave.end.price >= max(df[High])) and (wave.start.price <= min(df[Low]))
    elif wave.direction == direction.Short:
        return (wave.end.price <= min(df[Low])) and (wave.start.price >= max(df[High]))
    
def EXx_eq_SWx1(wave:wave, next_wave:wave)->bool:
    return wave.end.isEqual(next_wave.start)
           
def ESWx_take_HL_of_ES_candle(wave_direction:direction)-> Tuple[str,str]:
    if wave_direction == direction.Long:
        start_label = Low
        end_label = High
    elif wave_direction == direction.Short:
        start_label = High
        end_label = Low
    return start_label, end_label
