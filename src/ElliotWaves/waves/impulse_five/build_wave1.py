from typing import List, Tuple, Union
import pandas as pd
from ...direction import direction

from ...point import point
import logging

from ...wave import wave
from ...rules import rules

def __build_wave1(df:pd.DataFrame, impulse_direction: direction)-> Tuple[wave, direction]:
    if impulse_direction == direction.Long:
        start_label = "L"
        end_label = "H"
        wave_direction = direction.Long
    elif impulse_direction == direction.Short:
        start_label = "H"
        end_label = "L"
        wave_direction = direction.Short
    start_sr = df[start_label]
    end_sr = df[end_label]

    start_point = point(start_sr.index[0], start_sr[0])
    end_point = point(end_sr.index[-1], end_sr[-1])
    wave1 = wave(start_point,end_point)
    return wave1, wave_direction
    
def __check_wave1(wave1:wave,df: pd.DataFrame, wave_direction: direction)->Tuple[bool, List[str]]:
    return_status = True
    error_list = []
    
    if not rules.EWx_SWx_is_ext_RWx(wave1, df, wave_direction):
        error_list.append("EWx | SWx is extremum RWx: FAIL")
        return_status = False

    return return_status, error_list

def try_build_wave1(df:pd.DataFrame, impulse_direction: direction)->Tuple[bool, Union[wave, List[str]]]:
    logger = logging.getLogger("Try build wave 1")

    logger.debug("Build SW1 & EW1")

    wave1 = __build_wave1(df, impulse_direction)

    wave1, wave_direction = __build_wave1(df, impulse_direction)

    logger.debug("Start check rules wave 1")
    
    return_status, error_list = __check_wave1(wave1, df,wave_direction)
    
    if return_status:
        return return_status, wave1
    else:
        return return_status, error_list

def build_wave1(df:pd.DataFrame, impulse_direction: direction)->wave:
    logger = logging.getLogger("build wave 1")

    logger.info("Build SW1 & EW1")

    wave1, wave_direction = __build_wave1(df, impulse_direction)

    logger.info("Start check rules wave 1")

    return_status, error_list = __check_wave1(wave1, df,wave_direction)
    if return_status:   
        return wave1
    else:
        raise Exception("Wave check FAIL: \n"+"\n".join([("- " + err) for err in error_list]))