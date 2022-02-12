from typing import List
import pandas as pd

class NewCandleFlagBuilder:
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
    
    @staticmethod
    def get_flg_col(dt_sr: List[pd.Timestamp], comp_func)->pd.Series:
        worker = NewCandleFlagBuilder(comp_func)
        
        return pd.Series([worker.get_flag(idx) for idx in dt_sr],index=dt_sr,name=f"NewCandleFlag")

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
    
    @staticmethod
    def get_new_col(value_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
        worker = NewOpenColBuilder()
        return pd.DataFrame([value_sr, flag_sr]).transpose() \
        .apply(lambda row: worker.get_new(row[value_sr.name], row[flag_sr.name]), axis=1) \
        .rename(value_sr.name)
        
class NewCloseColBuilder:
    
    @staticmethod
    def get_new_col(value_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
        return value_sr.copy().rename(value_sr.name)

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
    
    @staticmethod
    def get_new_col(value_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
        worker = NewHighColBuilder()
        return pd.DataFrame([value_sr, flag_sr]).transpose() \
        .apply(lambda row: worker.get_new(row[value_sr.name], row[flag_sr.name]), axis=1) \
        .rename(value_sr.name)
        
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
    
    @staticmethod
    def get_new_col(value_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
        worker = NewLowColBuilder()
        return pd.DataFrame([value_sr, flag_sr]).transpose() \
        .apply(lambda row: worker.get_new(row[value_sr.name], row[flag_sr.name]), axis=1) \
        .rename(value_sr.name)

class NewVolumeColBuilder:
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
        else:
            self.prev_val = self.prev_val + value
        return self.prev_val
    
    @staticmethod
    def get_new_col(value_sr:pd.Series, flag_sr:pd.Series)->pd.Series:
        worker = NewVolumeColBuilder()
        return pd.DataFrame([value_sr, flag_sr]).transpose() \
            .apply(lambda row: worker.get_new(row[value_sr.name], row[flag_sr.name]), axis=1) \
            .rename(value_sr.name)
