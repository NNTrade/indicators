from enum import Enum

class TimeFrame(Enum):
    #TICKS = 1    
    MINUTES1 = 2
    MINUTES5 = 3
    MINUTES10 = 4
    MINUTES15 = 5
    MINUTES30 = 6
    HOURLY = 7
    DAILY = 8
    WEEKLY = 9
    MONTHLY = 10

    def __str__(self) -> str:
        if self == TimeFrame.MINUTES1:
            return "m1"
        elif self == TimeFrame.MINUTES5:
            return "m5"
        elif self == TimeFrame.MINUTES10:
            return "m10"
        elif self == TimeFrame.MINUTES15:
            return "m15"
        elif self == TimeFrame.MINUTES30:
            return "m30"
        elif self == TimeFrame.HOURLY:
            return "H"
        elif self == TimeFrame.DAILY:
            return "D"
        elif self == TimeFrame.WEEKLY:
            return "W"
        elif self == TimeFrame.MONTHLY:
            return "M"
        raise Exception(f"Unexpected TimeFrame {self}")