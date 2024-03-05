import unittest
import pandas as pd
import numpy as np
from src.ma.ema_builder import EmaBuilder as ema

class EmaBuilderTestCase(unittest.TestCase):

    def test_get_sr(self):
        base_sr = pd.Series([1,3,6],name="A")

        ema2 = ema(3)
        asserted_sr = ema2.get_for(base_sr)
        expected_sr = pd.Series([1,2,4])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            self.assertEqual(expected_sr[i], asserted_sr[i])
        
        self.assertEqual("EMA(3)[A]", asserted_sr.name)

    def test_get_sr_2(self):
        base_sr = pd.Series([2,1, 2,3, 4,5,6],name="B")
        is_last_sr = pd.Series([False,True, False,True, False,False,True])

        ema2 = ema(3)
        asserted_sr = ema2.get_for(base_sr,is_last_sr)
        expected_sr = pd.Series([2,1, 1.5,2, 3,3.5,4])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            self.assertEqual(expected_sr[i], asserted_sr[i])
        
        self.assertEqual("EMA(3)[B]", asserted_sr.name)
