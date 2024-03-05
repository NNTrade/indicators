import unittest
import pandas as pd
import numpy as np
from src.rsi import RSBuilder

class RSBuilderTestCase(unittest.TestCase):

    def test_get_sr(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,4],name="A")

        smag = RSBuilder(3)
        asserted_sr = smag.get_for(base_sr)
        gain_sr = pd.Series([
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
        
        loss_sr = pd.Series([
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
        expected_sr = pd.Series([
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

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertAlmostEqual(expected_sr[i], asserted_sr[i], 5, f"Error in index {i}")
        
        self.assertEqual("RS(3)[A]", asserted_sr.name)

    def test_get_sr_with_sub_calculated(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,4],name="A")

        smag = RSBuilder(3)
        
        gain_sr = pd.Series([
            2/1,
            2/1,
            (2+2)/2,
            (2+2+2)/3,
            (2+2+0)/3,
            (2+0+0)/3,
            (0+0+0)/3,
            (0+0+5)/3,
            (0+5+0)/3,
            (5+0+2)/3])
        
        loss_sr = pd.Series([
            1/1,
            0/1,
            (0+0)/2,
            (0+0+0)/3,
            (0+0+2)/3,
            (0+2+2)/3,
            (2+2+3)/3,
            (2+3+0)/3,
            (3+0+5)/3,
            (0+5+0)/3])
        asserted_sr = smag.get_for(base_sr,indicators_df=pd.DataFrame({"SmaGain(3)[A]":gain_sr, "SmaLoss(3)[A]":loss_sr}))
        expected_sr = pd.Series([
            2,
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

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertAlmostEqual(expected_sr[i], asserted_sr[i], 5, f"Error in index {i}")
        
        self.assertEqual("RS(3)[A]", asserted_sr.name)

    def test_get_sr_with_is_last(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,8],name="A")
        last_sr = pd.Series([0,1,0,1,0,1,0,1,0,1])

        smag = RSBuilder(3)
        asserted_sr = smag.get_for(base_sr,last_sr)
        gain_sr = pd.Series([
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
        loss_sr = pd.Series([
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
        expected_sr = pd.Series([
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

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertAlmostEqual(expected_sr[i], asserted_sr[i], 5, f"Error in index {i}")
        
        self.assertEqual("RS(3)[A]", asserted_sr.name)

    def test_get_sr_with_is_last_and_subcalculated(self):
        base_sr = pd.Series([3,5,7,9,7,5,2,7,2,8],name="A")
        last_sr = pd.Series([0,1,0,1,0,1,0,1,0,1])

        smag = RSBuilder(3)
        gain_sr = pd.Series([
            None,
            (2)/1,
            (2)/1,
            (4)/1,
            (4+0)/2,
            (4+0)/2,
            (4+0+0)/3,
            (4+0+2)/3,
            (0+2+0)/3,
            (0+2+1)/3])
        loss_sr = pd.Series([
            None,
            (1)/1,
            (0)/1,
            (0)/1,
            (0+2)/2,
            (0+4)/2,
            (0+4+3)/3,
            (0+4+0)/3,
            (4+0+5)/3,
            (4+0+0)/3])
        asserted_sr = smag.get_for(base_sr,indicators_df=pd.DataFrame({"SmaGain(3)[A]":gain_sr, "SmaLoss(3)[A]":loss_sr}))
        expected_sr = pd.Series([
            None,
            2,
            np.inf,
            np.inf,
            4/2,
            4/4,
            4/7,
            6/4,
            2/9,
            3/4])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            if np.isnan(expected_sr[i]):
                self.assertTrue(np.isnan(asserted_sr[i]))
            else:
                self.assertAlmostEqual(expected_sr[i], asserted_sr[i], 5, f"Error in index {i}")
        
        self.assertEqual("RS(3)[A]", asserted_sr.name)
