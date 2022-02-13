from pandas import Timestamp
import unittest
import pandas as pd
from pandas import Timestamp as datetime
import numpy as np
from src.candle_up_time_frame.builder import FirstInCandleFlagBuilder, NewOpenColBuilder, NewCloseColBuilder,NewLowColBuilder,NewHighColBuilder, NewVolumeColBuilder, LastInCandleFlagBuilder
from src.candle_up_time_frame.dt_compare import compare_strategy
from quote_source.client.TimeFrame import TimeFrame


class FirstInCandleFlagBuilderTestCase(unittest.TestCase):
    def test_get_flag(self):
        # Array
        df = pd.DataFrame(np.array([[1, 10, 3, 5, 10], [5, 9, 2, 8, 20], [6, 5, 15, 1, 30], [1, 10, 3, 5, 10], [1, 10, 3, 5, 10]]),
                          columns=["O", "H", "L", "C", "V"],
                          index=np.array([datetime(2000, 1, 1, 1), datetime(2000, 1, 1, 3), datetime(2000, 1, 2, 6), datetime(2000, 1, 2, 8), datetime(2000, 1, 2, 23)]))
        comp_func = compare_strategy(TimeFrame.D)
        expected_sr = pd.Series(
            [True, False, True, False, False], index=df.index)

        # Acts
        asserted_sr = FirstInCandleFlagBuilder.get_flg_col(df.index, comp_func)

        # Assert

        self.assertTrue(expected_sr.equals(asserted_sr))
        
class LastInCandleFlagBuilderTestCase(unittest.TestCase):
    def test_get_flag(self):
        # Array
        df = pd.DataFrame(np.array([[1, 10, 3, 5, 10], [5, 9, 2, 8, 20], [6, 5, 15, 1, 30], [1, 10, 3, 5, 10], [1, 10, 3, 5, 10]]),
                          columns=["O", "H", "L", "C", "V"],
                          index=np.array([datetime(2000, 1, 1, 1), datetime(2000, 1, 1, 3), datetime(2000, 1, 2, 6), datetime(2000, 1, 2, 8), datetime(2000, 1, 2, 23)]))
        comp_func = compare_strategy(TimeFrame.D)
        expected_sr = pd.Series(
            [ False,True, False, False, True], index=df.index)

        # Acts
        asserted_sr = LastInCandleFlagBuilder.get_flg_col(df.index, comp_func)

        # Assert

        self.assertTrue(expected_sr.equals(asserted_sr))

class NewOpenColBuilderTestCase(unittest.TestCase):
    def test_get_flag(self):
        # Array
        df = pd.DataFrame(np.array([[1, 10, 3, 5, 10], [5, 9, 2, 8, 20], [6, 5, 15, 1, 30], [1, 10, 3, 5, 10], [1, 10, 3, 5, 10]]),
                          columns=["O", "H", "L", "C", "V"],
                          index=np.array([datetime(2000, 1, 1, 1), datetime(2000, 1, 1, 3), datetime(2000, 1, 2, 6), datetime(2000, 1, 2, 8), datetime(2000, 1, 2, 23)]))
        flag_sr = pd.Series([True, False, True, False, False],
                            index=df.index, name="flg")
        expected_sr = pd.Series([1, 1, 6, 6, 6], index=df.index)

        # Acts
        asserted_sr = NewOpenColBuilder.get_new_col(df["O"], flag_sr)

        # Assert

        self.assertTrue(expected_sr.equals(asserted_sr))

class NewCloseColBuilderTestCase(unittest.TestCase):
    def test_get_flag(self):
        # Array
        df = pd.DataFrame(np.array([[1, 10, 3, 5, 10], [5, 9, 2, 8, 20], [6, 5, 15, 1, 30], [1, 10, 3, 5, 10], [1, 10, 3, 5, 10]]),
                          columns=["O", "H", "L", "C", "V"],
                          index=np.array([datetime(2000, 1, 1, 1), datetime(2000, 1, 1, 3), datetime(2000, 1, 2, 6), datetime(2000, 1, 2, 8), datetime(2000, 1, 2, 23)]))
        flag_sr = pd.Series([True, False, True, False, False],
                            index=df.index, name="flg")
        expected_sr = pd.Series([5, 8, 1, 5, 5], index=df.index)

        # Acts
        asserted_sr = NewCloseColBuilder.get_new_col(df["C"], flag_sr)

        # Assert

        self.assertTrue(expected_sr.equals(asserted_sr))
        
class NewLowColBuilderTestCase(unittest.TestCase):
    def test_get_flag(self):
        # Array
        df = pd.DataFrame(np.array([[1, 10, 3, 5, 10], [5, 9, 2, 8, 20], [6, 5, 15, 1, 30], [1, 10, 3, 5, 10], [1, 10, 10, 5, 10]]),
                          columns=["O", "H", "L", "C", "V"],
                          index=np.array([datetime(2000, 1, 1, 1), datetime(2000, 1, 1, 3), datetime(2000, 1, 2, 6), datetime(2000, 1, 2, 8), datetime(2000, 1, 2, 23)]))
        flag_sr = pd.Series([True, False, True, False, False],
                            index=df.index, name="flg")
        expected_sr = pd.Series([3, 2, 15, 3, 3], index=df.index)

        # Acts
        asserted_sr = NewLowColBuilder.get_new_col(df["L"], flag_sr)

        # Assert

        self.assertTrue(expected_sr.equals(asserted_sr))
        
class NewHighColBuilderTestCase(unittest.TestCase):
    def test_get_flag(self):
        # Array
        df = pd.DataFrame(np.array([[1, 10, 3, 5, 10], [5, 9, 2, 8, 20], [6, 5, 15, 1, 30], [1, 10, 3, 5, 10], [1, 7, 10, 5, 10]]),
                          columns=["O", "H", "L", "C", "V"],
                          index=np.array([datetime(2000, 1, 1, 1), datetime(2000, 1, 1, 3), datetime(2000, 1, 2, 6), datetime(2000, 1, 2, 8), datetime(2000, 1, 2, 23)]))
        flag_sr = pd.Series([True, False, True, False, False],
                            index=df.index, name="flg")
        expected_sr = pd.Series([10, 10, 5, 10, 10], index=df.index)

        # Acts
        asserted_sr = NewHighColBuilder.get_new_col(df["H"], flag_sr)

        # Assert

        self.assertTrue(expected_sr.equals(asserted_sr))
        
class NewVolumeColBuilderTestCase(unittest.TestCase):
    def test_get_flag(self):
        # Array
        df = pd.DataFrame(np.array([[1, 10, 3, 5, 10], [5, 9, 2, 8, 20], [6, 5, 15, 1, 20], [1, 10, 3, 5, 10], [1, 7, 10, 5, 10]]),
                          columns=["O", "H", "L", "C", "V"],
                          index=np.array([datetime(2000, 1, 1, 1), datetime(2000, 1, 1, 3), datetime(2000, 1, 2, 6), datetime(2000, 1, 2, 8), datetime(2000, 1, 2, 23)]))
        flag_sr = pd.Series([True, False, True, False, False],
                            index=df.index, name="flg")
        expected_sr = pd.Series([10, 30, 20, 30, 40], index=df.index)

        # Acts
        asserted_sr = NewVolumeColBuilder.get_new_col(df["V"], flag_sr)

        # Assert

        self.assertTrue(expected_sr.equals(asserted_sr))
        