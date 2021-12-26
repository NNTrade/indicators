from __future__ import annotations
import logging
from typing import List, Tuple
import pandas as pd
from .impulse_five_builder import builder
from .simple_wave_search import search_wave
from ..misc.direction import direction
from ..misc.wave import wave
from ..misc.candle_name import *


def search(df: pd.DataFrame, impulse_direction: direction = None, full_scan: bool = False) -> List[wave]:
    logger = logging.getLogger("Search")
    _ret = []
    while len(df.index) > 0:
        logger.info(f"Start search From {df.index[0]}")
        if impulse_direction == direction.Long or impulse_direction is None:
            _list, _ = __search(df, builder(direction.Long, True))
            _ret = _ret + _list
        if impulse_direction == direction.Short or impulse_direction is None:
            _list, _ = __search(
                df, builder(direction.Short, True))
            _ret = _ret + _list

        if full_scan and len(df.index) > 1:
            df = df[df.index >= df.index[1]]
        else:
            break
    return [b.build() for b in _ret]


def __search(df: pd.DataFrame, builder_imp_five: builder, try_search=False) -> Tuple[List[builder], List[builder]]:
    search_wv = search_wave(builder_imp_five.next_wave_direction)
    wave_list = search_wv.search(df, True)

    _ret = []
    _dead_ret = []

    for wave in wave_list:
        res, builder = builder_imp_five.try_add(wave)
        if res:
            if builder.isComplete:
                _ret.append(builder)
            else:
                _list, _dead_list = __search(
                    df[df.index >= wave.end.timestamp], builder)
                if len(_list) > 0:
                    _ret = _ret + _list
                elif try_search:
                    _dead_ret.append(builder)

                if len(_dead_list) > 0:
                    _dead_ret = _dead_ret + _dead_list

    return _ret, _dead_ret


def try_search(df: pd.DataFrame, impulse_direction: direction = None, full_scan: bool = False) -> Tuple[List[builder], List[builder]]:
    logger = logging.getLogger("Search")
    _ret = []
    _dead_ret = []
    while len(df.index) > 0:
        logger.info(f"Start search From {df.index[0]}")
        if impulse_direction == direction.Long or impulse_direction is None:
            _list, _dead_list = __search(df, builder(
                direction.Long, True), try_search=True)
            _ret = _ret + _list
            _dead_ret = _dead_ret + _dead_list
        if impulse_direction == direction.Short or impulse_direction is None:
            _list, _dead_list = __search(df, builder(
                direction.Short, True), try_search=True)
            _ret = _ret + _list
            _dead_ret = _dead_ret + _dead_list

        if full_scan and len(df.index) > 1:
            df = df[df.index >= df.index[1]]
        else:
            break
    return _ret, _dead_ret