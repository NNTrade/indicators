import unittest
import pandas as pd
import numpy as np
from src.gain_loss import SmaLossBuilder

class SmaLossBuilderTestCase(unittest.TestCase):

    def test_get_sr(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,4],name="A")

        smag = SmaLossBuilder(3)
        asserted_sr = smag.get_for(base_sr)
        expected_sr = pd.Series([
            None,
            0/1,
            (0+0)/2,
            (0+0+0)/3,
            (0+0+2)/3,
            (0+2+2)/3,
            (2+2+3)/3,
            (2+3+0)/3,
            (3+0+5)/3,
            (0+5+0)/3])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertEqual(expected_sr[i], asserted_sr[i],  f"Error in index {i}")
        
        self.assertEqual("SmaLoss(3)[A]", asserted_sr.name)

    def test_get_sr_with_is_last(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,8],name="A")
        last_sr = pd.Series([0,1,0,1,0,1,0,1,0,1])

        smag = SmaLossBuilder(3)
        asserted_sr = smag.get_for(base_sr,last_sr)
        expected_sr = pd.Series([
            None,
            None,
            (0)/1,
            (0)/1,
            (0+2)/2,
            (0+4)/2,
            (0+4+3)/3,
            (0+4+0)/3,
            (4+0+5)/3,
            (4+0+0)/3])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertEqual(expected_sr[i], asserted_sr[i],  f"Error in index {i}")
        
        self.assertEqual("SmaLoss(3)[A]", asserted_sr.name)
