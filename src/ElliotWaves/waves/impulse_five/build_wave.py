from typing import List, Tuple, Union
import pandas as pd
from ...misc.direction import direction
from ...misc.point import point
import logging
from ...misc.candle_name import * 
from ...misc.wave import wave
from ...rules import rules


def __build_wave(df: pd.DataFrame, wave_direction: direction) -> wave:
    if wave_direction == direction.Long:
        start_label = Low
        end_label = High
    elif wave_direction == direction.Short:
        start_label = High
        end_label = Low
    start_sr = df[start_label]
    end_sr = df[end_label]

    start_point = point(start_sr.index[0], start_sr[0])
    end_point = point(end_sr.index[-1], end_sr[-1])
    new_wave = wave(start_point, end_point)
    return new_wave


def __check_wave(wave: wave, df: pd.DataFrame, wave_direction: direction) -> Tuple[bool, List[str]]:
    return_status = True
    error_list = []

    if wave.direction != wave_direction:
        error_list.append(
            f"Wave direction is not {wave_direction}: FAIL")
        return_status = False

    if wave.time_is_sec == 0:
        error_list.append(
            f"Wave couldn't be in one candle: FAIL")
        return_status = False
        
    if not rules.EWx_SWx_is_ext_RWx(wave, df):
        error_list.append("EWx | SWx is extremum RWx: FAIL")
        return_status = False

    return return_status, error_list


def try_build_wave(df: pd.DataFrame, wave_direction: direction) -> Tuple[bool, Union[wave, List[str]]]:
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