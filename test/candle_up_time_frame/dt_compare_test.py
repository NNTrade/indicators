import unittest
import src.candle_up_time_frame.dt_compare as cf
from pandas import Timestamp

class Minutes15TestCas(unittest.TestCase):

    def test_next30(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=15, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=30, second=0)
        self.assertEqual(False, cf.minutes15(cur, prev))

    def test_next31(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=15, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=31, second=0)
        self.assertEqual(False, cf.minutes15(cur, prev))

    def test_next2959(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=15, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=29, second=59)
        self.assertEqual(True, cf.minutes15(cur, prev))

    def test_next0(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=30, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=0, second=0)
        self.assertEqual(False, cf.minutes15(cur, prev))

class Minutes15TestCas(unittest.TestCase):

    def test_next30(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=15, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=30, second=0)
        self.assertEqual(False, cf.minutes15(cur, prev))

    def test_next31(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=15, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=31, second=0)
        self.assertEqual(False, cf.minutes15(cur, prev))

    def test_next2959(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=15, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=29, second=59)
        self.assertEqual(True, cf.minutes15(cur, prev))

    def test_next0(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=30, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=0, second=0)
        self.assertEqual(False, cf.minutes15(cur, prev))


class Minutes10TestCas(unittest.TestCase):
    def test_next30(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=20, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=30, second=0)
        self.assertEqual(False, cf.minutes15(cur, prev))

    def test_next31(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=20, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=31, second=0)
        self.assertEqual(False, cf.minutes15(cur, prev))

    def test_next27(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=24, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=27, second=0)
        self.assertEqual(True, cf.minutes15(cur, prev))

class Minutes5TestCas(unittest.TestCase):
    def test_next10(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=7, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=10, second=0)
        self.assertEqual(False, cf.minutes5(cur, prev))
        self.assertEqual(False, cf.minutes5(prev, cur))

    def test_next959(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=7, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=9, second=59)
        self.assertEqual(True, cf.minutes5(cur, prev))
        self.assertEqual(True, cf.minutes5(prev, cur))

    def test_next0(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=3, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=0, second=0)
        self.assertEqual(True, cf.minutes5(cur, prev))
        self.assertEqual(True, cf.minutes5(prev, cur))

    def test_next60(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=57, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=11, minute=0, second=0)
        self.assertEqual(False, cf.minutes5(cur, prev))
        self.assertEqual(False, cf.minutes5(prev, cur))

    def test_next11(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=7, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=11, second=0)
        self.assertEqual(False, cf.minutes5(cur, prev))
        self.assertEqual(False, cf.minutes5(prev, cur))
    
    def test_next5(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=3, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=5, second=0)
        self.assertEqual(False, cf.minutes5(cur, prev))
        self.assertEqual(False, cf.minutes5(prev, cur))

    def test_next6(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=3, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=6, second=0)
        self.assertEqual(False, cf.minutes5(cur, prev))
        self.assertEqual(False, cf.minutes5(prev, cur))

    def test_next7(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=3, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=7, second=0)
        self.assertEqual(False, cf.minutes5(cur, prev))
        self.assertEqual(False, cf.minutes5(prev, cur))

    def test_next4(self):
        prev = Timestamp(year=2000, month=1, day=3, hour=10, minute=3, second=0)
        cur = Timestamp(year=2000, month=1, day=3, hour=10, minute=4, second=0)
        self.assertEqual(True, cf.minutes5(cur, prev))
        self.assertEqual(True, cf.minutes5(prev, cur))

class ShiftDataTestCas(unittest.TestCase):
    def test_get_shifted_month_data(self):
        dt_List = [Timestamp(year=2000, month=1, day=3), Timestamp(year=2000, month=1, day=30),Timestamp(year=2000, month=2, day=1)]

        self.assertTrue(cf.monthly(dt_List[1], dt_List[0]))
        self.assertTrue(not cf.monthly(dt_List[2], dt_List[1]))

    def test_get_shifted_minut_data(self):
        self.assertTrue(cf.minutes5(Timestamp(year=2000, month=1, day=3,hour=0,minute=2), Timestamp(year=2000, month=1, day=3,hour=0,minute=4)))
        self.assertTrue(not cf.minutes5(Timestamp(year=2000, month=1, day=3,hour=0,minute=2), Timestamp(year=2000, month=1, day=3,hour=0,minute=5)))
        self.assertTrue(not cf.minutes5(Timestamp(year=2000, month=1, day=3,hour=0,minute=2), Timestamp(year=2000, month=1, day=3,hour=0,minute=6)))

if __name__ == '__main__':
    unittest.main()
