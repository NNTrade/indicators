from datetime import time
from typing import List, Tuple
import unittest
import pandas as pd
import logging
from src.ElliotWaves.misc.direction import direction
from src.ElliotWaves.misc.point import point
from src.ElliotWaves.misc.wave import wave
from src.ElliotWaves.waves.impulse_five_builder import builder


class builder_TestCase(unittest.TestCase):

    def grow(arr: List[int], cur: int, times) -> Tuple[List[int], int]:
        for wave in range(times):
            arr.append(cur)
            cur = cur + 1
        return arr, cur

    def fall(arr: List[int], cur: int, times) -> Tuple[List[int], int]:
        for wave in range(times):
            arr.append(cur)
            cur = cur - 1
        return arr, cur

    def test_define_wave_long(self):

        high_arr, cur = builder_TestCase.grow([], 1, 3)
        high_arr, cur = builder_TestCase.fall(high_arr, cur, 2)
        high_arr, cur = builder_TestCase.grow(high_arr, cur, 7)
        high_arr, cur = builder_TestCase.fall(high_arr, cur, 3)
        high_arr, cur = builder_TestCase.grow(high_arr, cur, 10)

        # № | idx   |  ts   | pr H | pr L | Type  | W pr |
        # ---|-------|-------|------|------|-------|------|
        # 0 | 00-03 | 01-04 | 1-4  | 0-3  | Long  | 0-4  |
        # 1 | 03-05 | 04-06 | 4-2  | 3-1  | Short | 4-1  |
        # 2 | 05-12 | 06-13 | 2-9  | 1-8  | Long  | 1-9  |
        # 3 | 12-15 | 13-16 | 9-6  | 8-5  | Short | 9-5  |
        # 4 | 15-24 | 16-25 | 6-15 | 5-14 | Long  | 5-13 |

        times = []
        for day in range(len(high_arr)):
            times.append(pd.Timestamp(year=2021, month=1, day=day+1))

        low_arr = [h-1 for h in high_arr]

        df = pd.DataFrame(data={
            "H": high_arr,
            "L": low_arr},
            index=times)

        bif = builder(direction.Long)
        wave1 = wave(point(times[0], low_arr[0]), point(times[3], high_arr[3]))
        wave2 = wave(point(times[3], high_arr[3]), point(times[5], low_arr[5]))
        wave3 = wave(point(times[5], low_arr[5]),
                     point(times[12], high_arr[12]))
        wave4 = wave(point(times[12], high_arr[12]),
                     point(times[15], low_arr[15]))
        wave5 = wave(point(times[15], low_arr[15]),
                     point(times[24], high_arr[24]))

        with self.assertRaises(Exception):
            res, err = bif.try_add_wave2(wave2)
