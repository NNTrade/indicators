import unittest
from random import randrange
from pandas import Timestamp
from quote_source.client.TimeFrame import TimeFrame
import pandas as pd
import src.candle_up_time_frame.open_candle_dt as ocdt

class GetDtTestCase(unittest.TestCase):
    def test_get_Xmin(self):
        test_data = [
            (TimeFrame.MINUTE5, 5, [0,5,10,15,20,25,30,35,40,45,50,55]),
            (TimeFrame.MINUTE10, 10, [0,10,20,30,40,50]),
            (TimeFrame.MINUTE15, 15, [0,15,30,45]),
            (TimeFrame.MINUTE30, 30, [0,30])
        ]
        for test_datacase in test_data:
            for shift in range(test_datacase[1]):
                for base_val in test_datacase[2]:
                    base_dt = Timestamp(year=2020,month=3, day=5, hour=0, minute=base_val+shift)
                    asserted_dt:Timestamp = ocdt.get_open_candle_dt_func_strategy(test_datacase[0])(base_dt)
                    excepted_dt = Timestamp(year=2020,month=3, day=5, hour=0, minute=base_val)
                    self.assertEqual(excepted_dt, asserted_dt, f'Test [{test_datacase}]: from dt {base_dt} expect {excepted_dt} but get {asserted_dt}')

    def test_getHour(self):
        for min in range(60):
            hour = randrange(24)
            base_dt = Timestamp(year=2020,month=3, day=5, hour=hour, minute=min)
            asserted_dt:Timestamp = ocdt.get_open_candle_dt_func_strategy(TimeFrame.HOUR)(base_dt)
            excepted_dt = Timestamp(year=2020,month=3, day=5, hour=hour)
            self.assertEqual(excepted_dt, asserted_dt, f'from dt {base_dt} expect {excepted_dt} but get {asserted_dt}')

    def test_getDay(self):
        for min in range(60):
            for hour in range(24):
                day = randrange(1,30)
                base_dt = Timestamp(year=2020,month=3, day=day, hour=hour, minute=min)
                asserted_dt:Timestamp = ocdt.get_open_candle_dt_func_strategy(TimeFrame.DAY)(base_dt)
                excepted_dt = Timestamp(year=2020,month=3, day=day)
                self.assertEqual(excepted_dt, asserted_dt, f'from dt {base_dt} expect {excepted_dt} but get {asserted_dt}')

    def test_getMonth(self):
        for min in range(60):
            for hour in range(24):
                day = randrange(1,30)
                base_dt = Timestamp(year=2020,month=3, day=day, hour=hour, minute=min)
                asserted_dt:Timestamp = ocdt.get_open_candle_dt_func_strategy(TimeFrame.MONTH)(base_dt)
                excepted_dt = Timestamp(year=2020,month=3,day=1)
                self.assertEqual(excepted_dt, asserted_dt, f'from dt {base_dt} expect {excepted_dt} but get {asserted_dt}')

    def test_getWeek(self):
        data = [
            Timestamp(year=2021,month=8, day=30),
            Timestamp(year=2021,month=8, day=31),
            Timestamp(year=2021,month=9, day=1),
            Timestamp(year=2021,month=9, day=2),
            Timestamp(year=2021,month=9, day=3),
            Timestamp(year=2021,month=9, day=4),
            Timestamp(year=2021,month=9, day=5)
        ]
        for base_dt in data:
            asserted_dt:Timestamp = ocdt.get_open_candle_dt_func_strategy(TimeFrame.WEEK)(base_dt)
            excepted_dt = Timestamp(year=2021,month=8, day=30)
            self.assertEqual(excepted_dt, asserted_dt, f'from dt {base_dt} expect {excepted_dt} but get {asserted_dt}')

    def test_getWeek_2(self):
        data = [
            Timestamp(year=2021,month=9, day=6),
            Timestamp(year=2021,month=9, day=7),
            Timestamp(year=2021,month=9, day=8),
            Timestamp(year=2021,month=9, day=9),
            Timestamp(year=2021,month=9, day=10),
            Timestamp(year=2021,month=9, day=11),
            Timestamp(year=2021,month=9, day=12)
        ]
        for base_dt in data:
            asserted_dt:Timestamp = ocdt.get_open_candle_dt_func_strategy(TimeFrame.WEEK)(base_dt)
            excepted_dt = Timestamp(year=2021,month=9, day=6)
            self.assertEqual(excepted_dt, asserted_dt, f'from dt {base_dt} expect {excepted_dt} but get {asserted_dt}')

class GetOpenDTForSRTestCase(unittest.TestCase):
    def test_get_correct_sr(self):
        base_dt = pd.Series([Timestamp(2000,1,1,1,1), Timestamp(2000,1,1,1,3), Timestamp(2000,1,1,1,15), Timestamp(2000,1,1,1,20)])
        expect_dt = pd.Series([Timestamp(2000,1,1,1), Timestamp(2000,1,1,1), Timestamp(2000,1,1,1,15), Timestamp(2000,1,1,1,20)])
        assert_dt = ocdt.getOpenDTForSR(base_dt, TimeFrame.MINUTE5)
        self.assertTrue(expect_dt.equals(assert_dt))