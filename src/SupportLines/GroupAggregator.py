import pandas as pd

class GroupAggregator:
    def __init__(self, percent:float = 0.02) -> None:
        self.percent = percent
        pass

    def __filter_by_dev__(self, val:float, sr:pd.Series):
        dev = val * self.percent
        min_lim = val - dev
        max_lim = val + dev
        return (sr > min_lim) & (sr < max_lim)

    def aggregate(self,group_sr:pd.Series, value_sr:pd.Series )->pd.Series:
        return group_sr.apply(lambda g: value_sr[self.__filter_by_dev__(g,group_sr)].sum())