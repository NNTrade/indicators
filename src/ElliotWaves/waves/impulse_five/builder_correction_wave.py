from typing import List, Tuple, Union
import pandas as pd
from ...direction import direction

from ...point import point
import logging

from ...wave import wave
from ...rules import rules


def __build_corr_wave(df: pd.DataFrame, impulse_direction: direction) -> wave:
    if impulse_direction == direction.Long:
        start_label = "H"
        end_label = "L"
        wave_direction = direction.Short
    elif impulse_direction == direction.Short:
        start_label = "L"
        end_label = "H"
        wave_direction = direction.Long
    start_sr = df[start_label]
    end_sr = df[end_label]

    start_point = point(start_sr.index[0], start_sr[0])
    end_point = point(end_sr.index[-1], end_sr[-1])
    new_wave = wave(start_point, end_point)
    return new_wave, wave_direction


def __check_corr_wave(wave: wave, df: pd.DataFrame, impulse_direction: direction) -> Tuple[bool, List[str]]:
    return_status = True
    error_list = []

    if wave.direction != impulse_direction.revers():
        error_list.append(
            f"For {impulse_direction} correction wave should be {impulse_direction.revers()}: FAIL")
        return_status = False

    if not rules.EWx_SWx_is_ext_RWx(wave, df):
        error_list.append("EWx | SWx is extremum RWx: FAIL")
        return_status = False

    return return_status, error_list


def try_build_wave(df: pd.DataFrame, impulse_direction: direction) -> Tuple[bool, Union[wave, List[str]]]:
    logger = logging.getLogger("Try build correction wave")

    logger.debug("Build SW & EW")

    wave = __build_corr_wave(df, impulse_direction)

    wave, wave_direction = __build_corr_wave(df, impulse_direction)

    logger.debug("Start check rules correction wave")

    return_status, error_list = __check_corr_wave(wave, df, wave_direction)

    if return_status:
        return return_status, wave
    else:
        return return_status, error_list


def build_wave(df: pd.DataFrame, impulse_direction: direction) -> wave:
    logger = logging.getLogger("build correction wave")

    logger.info("Build SW & EW")

    wave = __build_corr_wave(df, impulse_direction)

    logger.info("Start check rules correction wave")

    return_status, error_list = __check_corr_wave(wave, df, impulse_direction)
    if return_status:
        return wave
    else:
        raise Exception("Wave check FAIL: \n" +
                        "\n".join([("- " + err) for err in error_list]))
