from typing import Tuple
import pandas as pd

def split_by_count(from_v:float, till_v:float, group_count:int, round:int = 5)->Tuple[float, pd.DataFrame]:
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
    groups_df = pd.DataFrame(groups, columns =['From', 'Till'])
    groups_df["GR"] = groups_df.round(round)[["From","Till"]].apply(tuple,axis=1)
    return interval, groups_df

def split_by_interval(from_v:float, till_v:float, group_interval:float, round:int = 5)->Tuple[float, pd.DataFrame]:
    groups = []
    cur_gr_min = from_v
    cur_gr_max = cur_gr_min+group_interval
    while cur_gr_min < till_v:
        groups.append((cur_gr_min, cur_gr_max))
        cur_gr_min = cur_gr_max
        cur_gr_max = cur_gr_min+group_interval
    groups[len(groups)-1] = (groups[len(groups)-1][0], till_v)
    groups_df = pd.DataFrame(groups, columns =['From', 'Till'])
    groups_df["GR"] = groups_df.round(round)[["From","Till"]].apply(tuple,axis=1)
    return group_interval, groups_df