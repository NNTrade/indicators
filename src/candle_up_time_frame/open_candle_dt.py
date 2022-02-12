from pandas import Timestamp, Timedelta
import pandas as pd
from quote_source.client.TimeFrame import TimeFrame

def get_open_candle_dt_func_strategy(tf:TimeFrame):
    if tf == TimeFrame.MONTH:
        return getOpenCandleDT_Month
    elif tf == TimeFrame.WEEK:
        return getOpenCandleDT_Week
    elif tf == TimeFrame.DAY:
        return getOpenCandleDT_Day
    elif tf == TimeFrame.HOUR:
        return getOpenCandleDT_Hour
    elif tf == TimeFrame.MINUTE30:
        return getOpenCandleDT_Min30
    elif tf == TimeFrame.MINUTE15:
        return getOpenCandleDT_Min15
    elif tf == TimeFrame.MINUTE10:
        return getOpenCandleDT_Min10
    elif tf == TimeFrame.MINUTE5:
        return getOpenCandleDT_Min5
    elif tf == TimeFrame.MINUTE:
        return getOpenCandleDT_Min1
    else:
        raise Exception(f"Unexpected TimeFrame {tf}")


def getOpenCandleDT_Month(dt:Timestamp)->Timestamp:
    return Timestamp(year=dt.year, month=dt.month,day=1)

def getOpenCandleDT_Week(dt:Timestamp)->Timestamp:
    ret_dt = Timestamp(year=dt.year, month=dt.month,day=dt.day)
    if dt.weekday() > 0:
        ret_dt = ret_dt - Timedelta(value=dt.weekday(), unit='day')
    return ret_dt

def getOpenCandleDT_Day(dt:Timestamp)->Timestamp:
    return Timestamp(year=dt.year, month=dt.month,day=dt.day)

def getOpenCandleDT_Hour(dt:Timestamp)->Timestamp:
    return Timestamp(year=dt.year, month=dt.month,day=dt.day,hour=dt.hour)

def getOpenCandleDT_Min1(dt:Timestamp)->Timestamp:
    return __getOpenCandleDT_MinX__(dt, 1)

def getOpenCandleDT_Min5(dt:Timestamp)->Timestamp:
    return __getOpenCandleDT_MinX__(dt, 5)

def getOpenCandleDT_Min10(dt:Timestamp)->Timestamp:
    return __getOpenCandleDT_MinX__(dt, 10)

def getOpenCandleDT_Min15(dt:Timestamp)->Timestamp:
    return __getOpenCandleDT_MinX__(dt, 15)

def getOpenCandleDT_Min30(dt:Timestamp)->Timestamp:
    return __getOpenCandleDT_MinX__(dt, 30)

def __getOpenCandleDT_MinX__(dt:Timestamp, mins:int)->Timestamp:
    return Timestamp(year=dt.year, month=dt.month,day=dt.day,hour=dt.hour,minute=dt.minute // mins * mins)

def getOpenDTForSR(dt_sr:pd.Series, tf:TimeFrame)->pd.Series:
    dt_getter = get_open_candle_dt_func_strategy(tf)
    return dt_sr.apply(lambda dt: dt_getter(dt))