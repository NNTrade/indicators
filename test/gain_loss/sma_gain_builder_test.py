import unittest
import pandas as pd
import numpy as np
from src.gain_loss import SmaGainBuilder

class SmaGainBuilderTestCase(unittest.TestCase):

    def test_get_sr(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,4],name="A")

        smag = SmaGainBuilder(3)
        asserted_sr = smag.get_for(base_sr)
        expected_sr = pd.Series([
            None,
            2/1,
            (2+2)/2,
            (2+2+2)/3,
            (2+2+0)/3,
            (2+0+0)/3,
            (0+0+0)/3,
            (0+0+5)/3,
            (0+5+0)/3,
            (5+0+2)/3])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertEqual(expected_sr[i], asserted_sr[i],  f"Error in index {i}")
        
        self.assertEqual("SmaGain(3)[A]", asserted_sr.name)

    def test_get_sr_with_is_last(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,8],name="A")
        last_sr = pd.Series([0,1,0,1,0,1,0,1,0,1])

        smag = SmaGainBuilder(3)
        asserted_sr = smag.get_for(base_sr,last_sr)
        expected_sr = pd.Series([
            None,
            None,
            (2)/1,
            (4)/1,
            (4+0)/2,
            (4+0)/2,
            (4+0+0)/3,
            (4+0+2)/3,
            (0+2+0)/3,
            (0+2+1)/3])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertEqual(expected_sr[i], asserted_sr[i],  f"Error in index {i}")
        
        self.assertEqual("SmaGain(3)[A]", asserted_sr.name)
