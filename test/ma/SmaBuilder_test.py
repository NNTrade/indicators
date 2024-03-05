import unittest
import pandas as pd
import numpy as np
from src.ma import SmaBuilder

class SmaBuilderTestCase(unittest.TestCase):

    def test_get_sr(self):
        base_sr = pd.Series([3,5,7,9,11],name="A")

        sma = SmaBuilder(3)
        asserted_sr = sma.get_for(base_sr)
        expected_sr = pd.Series([3,4,5,7,9])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            self.assertEqual(expected_sr[i], asserted_sr[i])
        
        self.assertEqual("SMA(3)[A]", asserted_sr.name)

    def test_get_sr_with_is_last(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,4],name="A")
        last_sr = pd.Series([0,1,0,1,0,1,0,1,0,1])

        sma = SmaBuilder(3)
        asserted_sr = sma.get_for(base_sr,last_sr)
        expected_sr = pd.Series([
            3/1,
            5/1,
            (5+7)/2,
            (5+9)/2,
            (5+9+7)/3,
            (5+9+5)/3,
            (9+5+2)/3,
            (9+5+7)/3,
            (5+7+2)/3,
            (5+7+4)/3])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            self.assertEqual(expected_sr[i], asserted_sr[i], f"Error in index {i}")
        
        self.assertEqual("SMA(3)[A]", asserted_sr.name)
