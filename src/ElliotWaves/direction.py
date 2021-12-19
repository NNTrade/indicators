from __future__ import annotations
from enum import Enum

class direction(Enum):
    Long = 1
    Short = 2
    Bull = 1
    Bear = 2
    Up = 1
    Down = 2
    Grow = 1
    Fall = 2

    def __str__(self) -> str:
        if self == direction.Long:
            return "Long"
        elif self == direction.Short:
            return "Short"
        raise Exception(f"Unexpected direction {self}")
    
    def revers(self)->direction:
        if self == direction.Long: return direction.Short
        elif self == direction.Short: return direction.Long
        raise Exception(f"Unexpected direction {self}")