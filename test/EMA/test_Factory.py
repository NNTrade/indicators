import unittest
import pandas as pd
from src.EMA.Factory import EmaFactory

class EmaFactoryTestCase(unittest.TestCase):
    def test_period_list(self):
        ema_f = EmaFactory([3,5])

        asserted_period_list = ema_f.periods
        expected_period_list = [3,5]

        self.assertEqual(len(asserted_period_list), len(expected_period_list))

        for i in range(len(expected_period_list)):
            self.assertEqual(expected_period_list[i], asserted_period_list[i])

    def test_ema_list(self):
        ema_f = EmaFactory([3,7])
        base_sr = pd.Series([1,3,7], name="a")
        
        asserted_emas = ema_f.getEma(base_sr)
        expected_emas = pd.concat([pd.Series([1,2,4.5],name="EMA3[a]"),pd.Series([1,1.5,2.875],name="EMA7[a]")],axis=1)

        self.assertEqual(len(asserted_emas.columns), len(expected_emas.columns))

        for c in expected_emas.columns:
            asserted_sr = asserted_emas[c]
            expected_sr = expected_emas[c]

            self.assertEqual(len(asserted_sr),len(expected_sr))

            for i in range(len(asserted_sr)):
                self.assertEqual(expected_sr[i], asserted_sr[i])

    def test_ema_list_2_is_last(self):
        ema_f = EmaFactory([3,7])
        base_sr = pd.Series([2,1, 2,3, 4,5,7],name="a")
        is_last_sr = pd.Series([False,True, False,True, False,False,True])

        asserted_emas = ema_f.getEma(base_sr, is_last_sr)
        expected_emas = pd.concat([pd.Series([2,1, 1.5,2, 3,3.5,4.5],name="EMA3[a]"),pd.Series([2,1, 1.25,1.5, 2.125,2.375,2.875],name="EMA7[a]")],axis=1)

        self.assertEqual(len(asserted_emas.columns), len(expected_emas.columns))

        for c in expected_emas.columns:
            asserted_sr = asserted_emas[c]
            expected_sr = expected_emas[c]

            self.assertEqual(len(asserted_sr),len(expected_sr))

            for i in range(len(asserted_sr)):
                self.assertEqual(expected_sr[i], asserted_sr[i])