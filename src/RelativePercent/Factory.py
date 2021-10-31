import pandas as pd
import typing

class PercentFactory:
    def __init__(self, use_abs:bool = False) -> None:
        self.use_abs:bool = use_abs
        pass

    @staticmethod
    def __get_name__(name)->str:
        if isinstance(name, typing.Iterable) and type(name) is not str and len(name) > 1:
            ret_name = "("
            for n in name:
                ret_name = ret_name+f"{n}"+","
            ret_name = ret_name[:-1] + ")"
            return ret_name
        else:
            return name
    
    def col_name(self,sr1:pd.Series, sr2:pd.Series)->str:
        return f"P[{PercentFactory.__get_name__(sr1.name)}-{PercentFactory.__get_name__(sr2.name)}]"

    def get(self,sr1:pd.Series,sr2:pd.Series)->pd.Series:        
        new_name = self.col_name(sr1=sr1, sr2=sr2)
        return get_percent(sr1=sr1,sr2=sr2,use_abs=self.use_abs).rename(new_name)

    def get_between_df(self, sr1_df:pd.DataFrame, sr2_df:pd.DataFrame)->pd.DataFrame:
        ret_sr_arr:typing.List[pd.Series] = []
        for c1 in sr1_df.columns:
            for c2 in sr2_df.columns:
                ret_sr_arr.append(self.get(sr1_df[c1],sr2_df[c2]))
        return pd.concat(ret_sr_arr, axis=1)

    def get_for_all_df(self, df:pd.DataFrame)->pd.DataFrame:
        ret_sr_arr:typing.List[pd.Series] = []
        for idx, cb2 in enumerate(df.columns):
            for cb1 in [c for c in df.columns[idx+1:] if c != cb2]:
                ret_sr_arr.append(self.get(df[cb1],df[cb2]))
        return pd.concat(ret_sr_arr, axis=1)

def get_percent(sr1:pd.Series,sr2:pd.Series, use_abs:bool = False)->pd.Series:
    """
    return pandas Series with percent sr1 - sr2 / sr2
    """
    ret_sr = ( sr1 - sr2 ) /sr2 * 100
    if use_abs:
        ret_sr = ret_sr.abs()
    return ret_sr