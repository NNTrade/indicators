from datetime import time
from typing import List, Tuple
import unittest
import pandas as pd
import logging
from src.ElliotWaves.misc.direction import direction
from src.ElliotWaves.misc.wave import wave
from src.ElliotWaves.waves.impulse_five_search import search

class search_TestCase(unittest.TestCase):
    
    def grow(arr:List[int], cur:int, times)-> Tuple[List[int], int]:
        for wave in range(times):
            arr.append(cur)
            cur = cur + 1
        return arr, cur

    def fall(arr:List[int], cur:int, times)-> Tuple[List[int], int]:
        for wave in range(times):
            arr.append(cur)
            cur = cur - 1
        return arr, cur
        
    def test_define_wave_long(self):
        
        high_arr,cur = search_TestCase.grow([], 1, 3)
        high_arr,cur = search_TestCase.fall(high_arr, cur, 2)
        high_arr,cur = search_TestCase.grow(high_arr, cur, 7)
        high_arr,cur = search_TestCase.fall(high_arr, cur, 3)
        high_arr,cur = search_TestCase.grow(high_arr, cur, 10)
        
        # № | idx   |  ts   | pr H | pr L | Type  | W pr |
        #---|-------|-------|------|------|-------|------|
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
        
        res = search(df,impulse_direction=direction.Long)
        self.assertTrue(len(res) == 1)
        
        def check_up(wv:wave,start_idx:int,end_idx:int):
            self.assertEqual(wv.start.timestamp.day,times[start_idx].day)
            self.assertEqual(wv.start.price,low_arr[start_idx])
            self.assertEqual(wv.end.timestamp,times[end_idx])
            self.assertEqual(wv.end.price,high_arr[end_idx])
        
        def check_down(wv:wave,start_idx:int,end_idx:int):
            self.assertEqual(wv.start.timestamp.day,times[start_idx].day)
            self.assertEqual(wv.start.price,high_arr[start_idx])
            self.assertEqual(wv.end.timestamp,times[end_idx])
            self.assertEqual(wv.end.price,low_arr[end_idx])
        
        series_five1 = res[0].sub_waves
        
        check_up(series_five1[0],0,3)
        check_down(series_five1[1],3,5)
        check_up(series_five1[2],5,12)
        check_down(series_five1[3],12,15)
        check_up(series_five1[4],15,24)
        
    def test_define_wave_short(self):
        
        cur = 15
        high_arr,cur = search_TestCase.fall([], cur, 9)
        high_arr,cur = search_TestCase.grow(high_arr, cur, 3)
        high_arr,cur = search_TestCase.fall(high_arr, cur, 7)
        high_arr,cur = search_TestCase.grow(high_arr, cur, 2)
        high_arr,cur = search_TestCase.fall(high_arr, cur, 4)
               
        # № | idx   |  ts   | pr H | pr L | Type  | W pr |
        #---|-------|-------|------|------|-------|------|
        # 0 | 00-09 | 01-10 | 15-6 | 14-5 | Short | 15-5 |
        # 1 | 09-12 | 10-13 | 6-9  | 5-8  | Long  | 5-9  |
        # 2 | 12-19 | 13-20 | 9-2  | 8-1  | Short | 9-1  |
        # 3 | 19-21 | 20-22 | 2-4  | 1-3  | Long  | 1-4  |
        # 4 | 21-24 | 22-25 | 4-1  | 3-0  | Short | 4-0  |
        
        times = []
        for day in range(len(high_arr)):
            times.append(pd.Timestamp(year=2021, month=1, day=day+1))
        
        low_arr = [h-1 for h in high_arr]
        
        df = pd.DataFrame(data={
            "H": high_arr,
            "L": low_arr},
            index=times)
        
        res = search(df,impulse_direction=direction.Short)
        self.assertTrue(len(res) == 1)
        
        def check_up(wv:wave,start_idx:int,end_idx:int):
            self.assertEqual(wv.start.timestamp.day,times[start_idx].day)
            self.assertEqual(wv.start.price,low_arr[start_idx])
            self.assertEqual(wv.end.timestamp,times[end_idx])
            self.assertEqual(wv.end.price,high_arr[end_idx])
        
        def check_down(wv:wave,start_idx:int,end_idx:int):
            self.assertEqual(wv.start.timestamp.day,times[start_idx].day)
            self.assertEqual(wv.start.price,high_arr[start_idx])
            self.assertEqual(wv.end.timestamp,times[end_idx])
            self.assertEqual(wv.end.price,low_arr[end_idx])
        
        series_five1 = res[0].sub_waves
        
        check_down(series_five1[0],0,9)
        check_up(series_five1[1],9,12)
        check_down(series_five1[2],12,19)
        check_up(series_five1[3],19,21)
        check_down(series_five1[4],21,24)
        
            
        
    
