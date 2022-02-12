import pandas as pd
from quote_source.client.TimeFrame import TimeFrame

def compare_strategy(tf: TimeFrame):
    if tf == TimeFrame.MONTH:
        return monthly
    elif tf == TimeFrame.WEEK:
        return weekly
    elif tf == TimeFrame.DAY:
        return daily
    elif tf == TimeFrame.HOUR:
        return hourly
    elif tf == TimeFrame.MINUTE30:
        return minutes30
    elif tf == TimeFrame.MINUTE15:
        return minutes15
    elif tf == TimeFrame.MINUTE10:
        return minutes10
    elif tf == TimeFrame.MINUTE5:
        return minutes5
    elif tf == TimeFrame.MINUTE:
        return minutes1
    else:
        raise Exception("Unexpected TimeFrame")

def monthly(date: pd.Timestamp, prev: pd.Timestamp):
    return prev is not None and date is not None and \
        date.year == prev.year and \
        date.month == prev.month


def weekly(date: pd.Timestamp, prev: pd.Timestamp):
    return prev is not None and date is not None and \
        date.year == prev.year and \
        date.month == prev.month and \
        date.weekofyear == prev.weekofyear


def daily(date: pd.Timestamp, prev: pd.Timestamp):
    return prev is not None and date is not None and \
        date.year == prev.year and \
        date.dayofyear == prev.dayofyear


def hourly(date: pd.Timestamp, prev: pd.Timestamp):
    return prev is not None and date is not None and \
        date.year == prev.year and \
        date.dayofyear == prev.dayofyear and \
        date.hour == prev.hour

def minutes30(date: pd.Timestamp, prev: pd.Timestamp):
    return prev is not None and date is not None and \
           __check_minute_part__(30,date, prev)

def minutes15(date: pd.Timestamp, prev: pd.Timestamp):
    return prev is not None and date is not None and \
           __check_minute_part__(15,date, prev)


def minutes10(date: pd.Timestamp, prev: pd.Timestamp):
    return prev is not None and date is not None and \
           __check_minute_part__(10,date, prev)


def minutes5(date: pd.Timestamp, prev: pd.Timestamp):
    return prev is not None and date is not None and \
           __check_minute_part__(5,date, prev)

def minutes1(date: pd.Timestamp, prev: pd.Timestamp):
    return prev is not None and date is not None and \
           abs((date - prev).total_seconds()) < 60 

def __check_minute_part__(range: int,date: pd.Timestamp, prev: pd.Timestamp):
    return abs((date - prev).total_seconds()) < range*60 and \
           (date.minute // range == prev.minute // range) 