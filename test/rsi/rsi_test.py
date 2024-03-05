import unittest
import pandas as pd
import numpy as np
from src.rsi import RSIBuilder

class RSIBuilderTestCase(unittest.TestCase):

    def test_get_sr(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,4],name="A")

        smag = RSIBuilder(3)
        asserted_sr = smag.get_for(base_sr)
        rs_sr = pd.Series([
            None,
            np.inf,
            np.inf,
            np.inf,
            4/2,
            2/4,
            0,
            5/5,
            5/8,
            7/5
        ])
        expected_sr = pd.Series([
            None,
            100,
            100,
            100,
            100 - 100 / 3,
            100 - 100 / 1.5,
            100 - 100 / 1,
            100 - 100 / 2,
            100 - 100 / (1 + 5/8),
            100 - 100 / (1 + 7/5)
        ])
        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertAlmostEqual(expected_sr[i], asserted_sr[i], 5, f"Error in index {i}")
        
        self.assertEqual("RSI(3)[A]", asserted_sr.name)

    def test_get_sr_with_subculculated(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,4],name="A")

        smag = RSIBuilder(3)        
        rs_sr = pd.Series([
            None,
            np.inf,
            np.inf,
            4,
            4/2,
            2/4,
            0,
            5/5,
            5/8,
            7/5
        ])
        asserted_sr = smag.get_for(base_sr, indicators_df=pd.DataFrame({"RS(3)[A]":rs_sr}))
        expected_sr = pd.Series([
            None,
            100,
            100,
            100 - 100 / (1 + 4),
            100 - 100 / 3,
            100 - 100 / 1.5,
            100 - 100 / 1,
            100 - 100 / 2,
            100 - 100 / (1 + 5/8),
            100 - 100 / (1 + 7/5)
        ])
        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertAlmostEqual(expected_sr[i], asserted_sr[i], 5, f"Error in index {i}")
        
        self.assertEqual("RSI(3)[A]", asserted_sr.name)
    
    def test_get_sr_with_is_last(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,8],name="A")
        last_sr = pd.Series([0,1,0,1,0,1,0,1,0,1])

        smag = RSIBuilder(3)
        asserted_sr = smag.get_for(base_sr,last_sr)
        rs_sr = pd.Series([
            None,
            None,
            np.inf,
            np.inf,
            4/2,
            4/4,
            4/7,
            6/4,
            2/9,
            3/4])
        expected_sr = pd.Series([
            None,
            None,
            100,
            100,
            100 - 100 / 3,
            100 - 100 / 2,
            100 - 100 / (1 + 4/7),
            100 - 100 / (1 + 6/4),
            100 - 100 / (1 + 2/9),
            100 - 100 / (1 + 3/4),
        ])
        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertAlmostEqual(expected_sr[i], asserted_sr[i], 5, f"Error in index {i}")
        
        self.assertEqual("RSI(3)[A]", asserted_sr.name)

    def test_get_sr_with_is_last_and_subcalculated(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,8],name="A")
        last_sr = pd.Series([0,1,0,1,0,1,0,1,0,1])

        smag = RSIBuilder(3)
        
        rs_sr = pd.Series([
            None,
            None,
            np.inf,
            1,
            4/2,
            4/4,
            4/7,
            6/4,
            2/9,
            3/4])
        asserted_sr = smag.get_for(base_sr,last_sr, pd.DataFrame({"RS(3)[A]":rs_sr}))
        expected_sr = pd.Series([
            None,
            None,
            100,
            100 - 100 / (1+1),
            100 - 100 / 3,
            100 - 100 / 2,
            100 - 100 / (1 + 4/7),
            100 - 100 / (1 + 6/4),
            100 - 100 / (1 + 2/9),
            100 - 100 / (1 + 3/4),
        ])
        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertAlmostEqual(expected_sr[i], asserted_sr[i], 5, f"Error in index {i}")
        
        self.assertEqual("RSI(3)[A]", asserted_sr.name)

    
