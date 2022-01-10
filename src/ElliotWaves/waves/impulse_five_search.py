from __future__ import annotations
import logging
from typing import List, Tuple
import pandas as pd
from .impulse_five_builder import builder
from .simple_wave_search import search_wave
from ..misc.direction import direction
from ..misc.wave import wave
from ..misc.candle_name import *

def condens_sub_waves(wave_list:List[wave])->List[List[wave]]:
    """Преобразует найденные серии волн в массив подволн. Если волна не имеет подволны, то преобразуем ее в массив с одной волной

    Args:
        wave_list (List[wave]): список найденных волн

    Returns:
        List[List[wave]]: Массив серии волн
    """
    _ret_wave_list:List[List[wave]] = []
    for dead in wave_list:
        sb_wv = dead.sub_waves
        if len(sb_wv) == 0:
            _ret_wave_list.append([dead])
        else:
            _ret_wave_list.append(sb_wv)
    return _ret_wave_list

def search(df: pd.DataFrame, impulse_direction: direction = None, full_scan: bool = False) -> Tuple[List[wave], List[wave]]:
    """Ищем возможные волны на участке

    Args:
        df (pd.DataFrame): участок на котором необходимо найти волны
        impulse_direction (direction, optional): Направление поиска. Defaults to None.
        full_scan (bool, optional): полное сканирование участка. Defaults to False.

    Returns:
        Tuple[List[wave], List[wave]]: Кортеж(список завершенных волн, список мертвых волн)
    """
    logger = logging.getLogger("Search")
    _ret: List[builder] = []
    _dead_ret: List[builder] = []
    while len(df.index) > 0:
        logger.info(f"Start search From {df.index[0]}")
        if impulse_direction == direction.Long or impulse_direction is None:
            _list, _dead_list = __search(
                df, builder(direction.Long, True))
            _ret = _ret + _list
            _dead_ret = _dead_ret + _dead_list
        if impulse_direction == direction.Short or impulse_direction is None:
            _list, _dead_list = __search(
                df, builder(direction.Short, True))
            _ret = _ret + _list
            _dead_ret = _dead_ret + _dead_list
            
        if full_scan and len(df.index) > 1:
            df = df[df.index >= df.index[1]]
        else:
            break
    return ([b.build() for b in _ret],[b.build() for b in _dead_ret])

def research(df: pd.DataFrame, unclosed_waves:List[wave], impulse_direction: direction = None, full_scan: bool = False) -> Tuple[List[wave], List[wave]]:
    return NotImplementedError()

def __search(df: pd.DataFrame, builder_imp_five: builder) -> Tuple[List[builder], List[builder]]:
    """Ищем следующую волну в серии на участке

    Args:
        df (pd.DataFrame):  участок на котором необходимо найти волну
        builder_imp_five (builder): строитель 5 волновой структуры

    Returns:
        Tuple[List[builder], List[builder]]: Кортеж(Список полных вол, Список незавершенных волн)
    """
    
    search_wv = search_wave(builder_imp_five.next_wave_direction)
    wave_list:List[wave] = search_wv.search(df, True)

    _ret:List[builder] = []
    _dead_ret:List[builder] = []
    
    _ret, _dead_ret = __check_found_waves(df, builder_imp_five, wave_list, _ret, _dead_ret)

    return _ret, _dead_ret

def __check_found_waves(df:pd.DataFrame, builder_imp_five:builder, wave_list:List[wave], _success_ret:List[builder], _dead_ret:List[builder])-> Tuple[List[builder],List[builder]]:
    """Проверяем найденные волны, проверяем кто из них приводит к полной 5-ти волновой структуре, а кто нет

    Args:
        df (pd.DataFrame): участок на котором проверяются волны
        builder_imp_five (builder): строитель 5-ти волновой структуры
        wave_list (List[wave]): [description]
        _ret (List[builder]): [description]
        _dead_ret (List[builder]): [description]

    Returns:
        Tuple[List[builder],List[builder]]: [description]
    """
    for wave in wave_list:
        res, builder = builder_imp_five.try_add(wave)
        if res:
            ## если 5-ти волновая структура завершена, добавляем ее в список успешных волн
            if builder.isComplete:
                _success_ret.append(builder)
            ## если не завершена, продолжаем собирать
            else:
                _success_list, _dead_list = __search(
                    df[df.index >= wave.end.timestamp], builder)
                # Если у волны есть развитие, то добавляем ее в успешные
                if len(_success_list) > 0:
                    _success_ret = _success_ret + _success_list
                # Если у волны нет развития, то добавляем ее в мертвые
                else:
                    _dead_ret.append(builder)

                # Если у волны есть тупиковые развития добавляем их
                if len(_dead_list) > 0:
                    _dead_ret = _dead_ret + _dead_list
                    
    return _success_ret,_dead_ret


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
