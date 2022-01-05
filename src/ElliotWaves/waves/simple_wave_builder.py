from typing import List, Tuple, Union
import pandas as pd
import logging
from ..misc.direction import direction
from ..misc.point import point
from ..misc.candle_name import * 
from ..misc.wave import wave
from ..rules import rules


def __build_wave(df: pd.DataFrame, wave_direction: direction) -> wave:
    '''
    Создать инстанцую волны (wave) на указанном отрезке df в указанном напрвлении wave_directian
    '''
    start_label,end_label = rules.ESWx_take_HL_of_ES_candle(wave_direction)
    start_sr = df[start_label]
    end_sr = df[end_label]

    start_point = point(start_sr.index[0], start_sr[0])
    end_point = point(end_sr.index[-1], end_sr[-1])
    new_wave = wave(start_point, end_point)
    return new_wave


def __check_wave(wave: wave, df: pd.DataFrame, wave_direction: direction) -> Tuple[bool, List[str]]:
    '''
    Проверить, что построенная полна удовлетворяет правилам
    '''
    return_status = True
    error_list = []

    ## направление созданный волны = требуемому направлению    
    if wave.direction != wave_direction:
        error_list.append(
            f"Wave direction is not {wave_direction}: FAIL")
        return_status = False

    ## длина волны > 1 свечи
    if wave.time_is_sec == 0:
        error_list.append(
            f"Wave couldn't be in one candle: FAIL")
        return_status = False
    
    if not rules.EWx_SWx_is_ext_RWx(wave, df):
        error_list.append("EWx | SWx is extremum RWx: FAIL")
        return_status = False

    return return_status, error_list


def try_build_wave(df: pd.DataFrame, wave_direction: direction) -> Tuple[bool, Union[wave, List[str]]]:
    '''
    Попытаться построить волну на указанном отрезке df в указанном напрвлении wave_directian
    '''
    logger = logging.getLogger("try_build_wave")
    logger.debug(f"Try build {wave_direction} wave from {df.index[0]} till {df.index[-1]}")

    wave = __build_wave(df, wave_direction)

    logger.debug(f"Start check base wave rules")

    return_status, error_list = __check_wave(wave, df, wave_direction)

    if return_status:
        logger.debug(f"Wave build {wave}")
        return return_status, wave
    else:
        return return_status, error_list


def build_wave(df: pd.DataFrame, wave_direction: direction) -> wave:
    '''
    Построить волну на указанном отрезке df в указанном напрвлении wave_directian
    '''
    logger = logging.getLogger(f"build_wave")

    logger.debug(f"Build {wave_direction} wave from {df.index[0]} till {df.index[-1]}")

    wave = __build_wave(df, wave_direction)

    logger.debug(f"Start check base wave rules")

    return_status, error_list = __check_wave(wave, df, wave_direction)
    if return_status:
        logger.debug(f"Wave build {wave}")
        return wave
    else:
        logger.debug(f"Get error while build {wave}")
        errors = "Wave check FAIL: \n" + "\n".join([("- " + err) for err in error_list])
        logger.debug(errors)
        raise Exception(errors)
