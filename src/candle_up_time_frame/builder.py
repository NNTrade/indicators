from typing import List
import pandas as pd

def get_first_in_candle_flag(dt_sr: List[pd.Timestamp], comp_func)->pd.Series:
    """
    Получить колонку с флагом, что начинается новая свеча верхнего уровня
    """
    class FirstInCandleFlagBuilder2:
        """
        Строитель колонки с флагом, что начинается новая свеча верхнего уровня
        """
        def __init__(self, compare_func):
            """

            Args:
                compare_func ([type]): функция определения, что началась новая свеча
            """
            self._compare_func = compare_func
            self._prev_date = None
        
        def get_flag(self, dt:pd.Timestamp)->bool:
            """Проверить время на признак, что это новая свеча

            Args:
                dt (pd.Timestamp): временная метка начала свечи

            Returns:
                bool: флаг с результатом
            """
            if not self._compare_func(dt, self._prev_date):
                self._prev_date = dt
                return True
            else:
                return False
    worker = FirstInCandleFlagBuilder2(comp_func)
        
    return pd.Series([worker.get_flag(idx) for idx in dt_sr],index=dt_sr,name=f"NewCandleFlag")

def get_last_in_candle_flag(dt_sr: List[pd.Timestamp], comp_func)->pd.Series:
    """
    Получить колонку с флагом, конца свечи верхнего уровня
    """
    return get_first_in_candle_flag(dt_sr, comp_func).shift(periods=-1, fill_value=True)

def get_new_open_col(value_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
    """
    Получить новую колонку Open
    """
    class NewOpenColBuilder:
        """
        Строитель новой колонки Open
        """
        def __init__(self) -> None:
            self.prev_val = None
            pass
        
        def get_new(self,value:float, flag:bool)->float:
            """Получть новое значение

            Args:
                value (float): текущее значение
                flag (bool): значение флага

            Returns:
                float: новое значение
            """
            if flag or self.prev_val is None:
                self.prev_val = value
            return self.prev_val
    
    worker = NewOpenColBuilder()
    return pd.DataFrame([value_sr, flag_sr]).transpose() \
        .apply(lambda row: worker.get_new(row[value_sr.name], row[flag_sr.name]), axis=1) \
        .rename(value_sr.name)

def get_new_close_col(value_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
    """
    Получить новую колонку Close
    """
    return value_sr.copy().rename(value_sr.name)

def get_new_high_col(value_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
    """
    Получить новую колонку High
    """ 
    class NewHighColBuilder:
        """
        Строитель новой колонки High
        """
        def __init__(self) -> None:
            self.prev_val = None
            pass
        
        def get_new(self,value:float, flag:bool)->float:
            """Получть новое значение

            Args:
                value (float): текущее значение
                flag (bool): значение флага

            Returns:
                float: новое значение
            """
            if flag or self.prev_val is None:
                self.prev_val = value
            self.prev_val = max(self.prev_val, value)
            return self.prev_val
    
    worker = NewHighColBuilder()
    return pd.DataFrame([value_sr, flag_sr]).transpose() \
        .apply(lambda row: worker.get_new(row[value_sr.name], row[flag_sr.name]), axis=1) \
        .rename(value_sr.name)
    
def get_new_low_col(value_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
    """
    Получить новую колонку Low
    """ 
    class NewLowColBuilder:
        """
        Строитель новой колонки Low
        """
        def __init__(self) -> None:
            self.prev_val = None
            pass
        
        def get_new(self,value:float, flag:bool)->float:
            """Получть новое значение

            Args:
                value (float): текущее значение
                flag (bool): значение флага

            Returns:
                float: новое значение
            """
            if flag or self.prev_val is None:
                self.prev_val = value
            self.prev_val = min(self.prev_val, value)
            return self.prev_val
        
    worker = NewLowColBuilder()
    return pd.DataFrame([value_sr, flag_sr]).transpose() \
        .apply(lambda row: worker.get_new(row[value_sr.name], row[flag_sr.name]), axis=1) \
        .rename(value_sr.name)

def get_new_volume_col(value_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
    """
    Получить новую колонку Volume
    """ 
    class NewVolumeColBuilder:
        """
        Строитель новой колонки Volume
        """
        def __init__(self) -> None:
            self.prev_val = None
            pass
        
        def get_new(self,value:float, flag:bool)->float:
            """Получть новое значение

            Args:
                value (float): текущее значение
                flag (bool): значение флага

            Returns:
                float: новое значение
            """
            if flag or self.prev_val is None:
                self.prev_val = value
            else:
                self.prev_val = self.prev_val + value
            return self.prev_val
    
    worker = NewVolumeColBuilder()
    return pd.DataFrame([value_sr, flag_sr]).transpose() \
            .apply(lambda row: worker.get_new(row[value_sr.name], row[flag_sr.name]), axis=1) \
            .rename(value_sr.name)
