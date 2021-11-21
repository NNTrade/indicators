from typing import Tuple
import pandas as pd

group_col_name = "GR"
from_col_name = "From"
till_col_name = "Till"

def split_by_count(from_v:float, till_v:float, group_count:int, round:int = None)->Tuple[float, pd.DataFrame]:
    interval = (till_v - from_v)/group_count
    groups = []
    cur_gr_min = from_v
    cur_gr_max = cur_gr_min+interval
    idx = 1
    while idx < group_count:
        groups.append((cur_gr_min, cur_gr_max))
        cur_gr_min = cur_gr_max
        cur_gr_max = cur_gr_min+interval
        idx = idx + 1 
    groups.append((cur_gr_min, till_v))
    groups_df = pd.DataFrame(groups, columns =[from_col_name, till_col_name])
    if round is not None:
        groups_df = groups_df.round(round)
    groups_df[group_col_name] = groups_df[[from_col_name,till_col_name]].apply(tuple,axis=1)
    return interval, groups_df

def split_by_interval(from_v:float, till_v:float, group_interval:float, round:int = None)->Tuple[float, pd.DataFrame]:
    groups = []
    cur_gr_min = from_v
    cur_gr_max = cur_gr_min+group_interval
    while cur_gr_min < till_v:
        groups.append((cur_gr_min, cur_gr_max))
        cur_gr_min = cur_gr_max
        cur_gr_max = cur_gr_min+group_interval
    groups[len(groups)-1] = (groups[len(groups)-1][0], till_v)
    groups_df = pd.DataFrame(groups, columns =[from_col_name, till_col_name])
    if round is not None:
        groups_df = groups_df.round(round)
    groups_df[group_col_name] = groups_df[[from_col_name,till_col_name]].apply(tuple,axis=1)
    return group_interval, groups_df

def classify_price_sr_by_group(pv_sr:pd.Series,groups_sr:pd.Series)->pd.Series:
    return pv_sr.apply(lambda pv: classify_price_by_group(pv, groups_sr))

def classify_price_by_group(pv,groups_sr:pd.Series):
    find_groups = groups_sr[groups_sr.apply(lambda gr: pv > gr[0] and pv <= gr[1])]
    if len(find_groups) != 1:
        if pv == groups_sr[0][0]:
            return 1
        raise Exception(f"Cann't define group for value {pv}, get {len(find_groups)} groups")
    try:
        return find_groups.index[0]+1
    except:
        raise Exception(f"Cann't define group for value {pv}, get {len(find_groups)} groups")