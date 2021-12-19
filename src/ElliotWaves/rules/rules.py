import pandas as pd

from src.ElliotWaves.direction import direction

from ..wave import wave
from ..direction import direction

def __direction_adapter__(base_compare: bool, direction: direction)-> bool:
    if direction == direction.Long: return base_compare
    if direction == direction.Short: return not base_compare
    raise Exception(f"unknown direction {direction}")

def ex_check(name:str, function_return:bool):
    if not function_return:
        raise Exception(f"{name}: FAIL")

def EW2_gt_SW1(wave2: wave, wave1: wave, direction: direction)->bool:
    ret = wave2.end.price > wave1.start.price
    return __direction_adapter__(ret, direction)

def EW3_gt_EW1(wave3: wave, wave1: wave, direction: direction)->bool:
    ret = wave3.end.price > wave1.end.price
    return __direction_adapter__(ret, direction)

def HW3_gt_HW1_or_HW3_gt_HW5(wave1:wave, wave3:wave, wave5:wave)->bool:
    return wave3.height > wave1.height or wave3.height > wave5.height

def EW5_gt_EW3(wave3: wave, wave5: wave, direction: direction)->bool:
    ret = wave3.end.price > wave5.end.price
    return __direction_adapter__(ret, direction)

def W2_dif_W4(wave2: wave, wave4: wave)->bool:
    return wave2.height != wave4.height or wave2.time != wave4.time or wave2.type != wave4.type