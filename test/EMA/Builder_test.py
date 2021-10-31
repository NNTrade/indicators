import unittest
import pandas as pd
import numpy as np
from src.EMA.Builder import EmaBuilder as ema

class EmaBuilderTestCase(unittest.TestCase):

    def test_get(self):
        df = pd.DataFrame(np.array([[1, 2, 3], [3, 4, 6], [6, 9, 9]]),
                   columns=['a', 'b', 'c'])

        ema2 = ema(3)
        emaCols = ema2.getDf(df[["a","b"]])
        
        self.assertEqual(1, df["a"][0])
        self.assertEqual(3, df["a"][1])
        self.assertEqual(6, df["a"][2])

        self.assertEqual(2, df["b"][0])
        self.assertEqual(4, df["b"][1])
        self.assertEqual(9, df["b"][2])

        self.assertEqual(1, emaCols["EMA3[a]"][0])
        self.assertEqual(2, emaCols["EMA3[a]"][1])
        self.assertEqual(4, emaCols["EMA3[a]"][2])

        self.assertEqual(2, emaCols["EMA3[b]"][0])
        self.assertEqual(3, emaCols["EMA3[b]"][1])
        self.assertEqual(6, emaCols["EMA3[b]"][2])
        
    def test_get_tuple_col(self):
        df = pd.concat(
            { 
                'col1': pd.DataFrame(np.array([[1, 2], [3, 4], [6, 9]]),columns=['a','b']),
                'col2': pd.DataFrame(np.array([3,6,9]),columns=['c'])
            }, 
            axis=1)  
        
        ema2 = ema(3)
        emaCols = ema2.getDf(df[[('col1', "a"), ("col1", "b")]])
        self.assertEqual(1, df[("col1","a")][0])
        self.assertEqual(3, df[("col1","a")][1])
        self.assertEqual(6, df[("col1","a")][2])

        self.assertEqual(2, df[("col1","b")][0])
        self.assertEqual(4, df[("col1","b")][1])
        self.assertEqual(9, df[("col1","b")][2])

        self.assertEqual(1, emaCols[('col1',"EMA3[a]")][0])
        self.assertEqual(2, emaCols[('col1',"EMA3[a]")][1])
        self.assertEqual(4, emaCols[('col1',"EMA3[a]")][2])

        self.assertEqual(2, emaCols[('col1',"EMA3[b]")][0])
        self.assertEqual(3, emaCols[('col1',"EMA3[b]")][1])
        self.assertEqual(6, emaCols[('col1',"EMA3[b]")][2])

    def test_get_multi_tuple_col(self):
        df = pd.concat(
            { 
                'col1': pd.concat(
                    { 
                        'col11': pd.DataFrame(np.array([[1, 2], [3, 4], [6, 9]]),columns=['a','b']),
                        'col12': pd.DataFrame(np.array([3,6,9]),columns=['c'])
                    }, axis=1), 
                'col2':pd.concat(
                    { 
                        "col21": pd.DataFrame(np.array([3,6,9]),columns=['c']) 
                    }, axis=1)
            }, 
            axis=1)  
        
        ema2 = ema(3)
        emaCols = ema2.getDf(df[[('col1', 'col11',"a"), ("col1",'col11', "b")]])
        self.assertEqual(1, df[("col1",'col11',"a")][0])
        self.assertEqual(3, df[("col1",'col11',"a")][1])
        self.assertEqual(6, df[("col1",'col11',"a")][2])

        self.assertEqual(2, df[("col1",'col11',"b")][0])
        self.assertEqual(4, df[("col1",'col11',"b")][1])
        self.assertEqual(9, df[("col1",'col11',"b")][2])

        self.assertEqual(1, emaCols[('col1','col11',"EMA3[a]")][0])
        self.assertEqual(2, emaCols[('col1','col11',"EMA3[a]")][1])
        self.assertEqual(4, emaCols[('col1','col11',"EMA3[a]")][2])

        self.assertEqual(2, emaCols[('col1','col11',"EMA3[b]")][0])
        self.assertEqual(3, emaCols[('col1','col11',"EMA3[b]")][1])
        self.assertEqual(6, emaCols[('col1','col11',"EMA3[b]")][2])

    def test_get_sr(self):
        base_sr = pd.Series([1,3,6])

        ema2 = ema(3)
        asserted_sr = ema2.getSr(base_sr)
        expected_sr = pd.Series([1,2,4])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            self.assertEqual(expected_sr[i], asserted_sr[i])

    def test_get_sr_2(self):
        base_sr = pd.Series([2,1, 2,3, 4,5,6])
        is_last_sr = pd.Series([False,True, False,True, False,False,True])

        ema2 = ema(3)
        asserted_sr = ema2.getSr(base_sr,is_last_sr)
        expected_sr = pd.Series([2,1, 1.5,2, 3,3.5,4])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            self.assertEqual(expected_sr[i], asserted_sr[i])

    def test_get_sr_name(self):
        base_df = pd.DataFrame(np.array([[1, 2, 3], [3, 4, 6], [6, 9, 9]]),
                   columns=['a', 'b', 'c'])

        ema2 = ema(3)
        asserted_sr = ema2.getSr(base_df["a"])
        expected_sr = pd.Series([1,2,4])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            self.assertEqual(expected_sr[i], asserted_sr[i])
        
        self.assertEqual(ema2.expect_name("a"), asserted_sr.name)
        self.assertEqual("EMA3[a]", asserted_sr.name)

    def test_get_sr_name_from_sr(self):
        base_sr = pd.Series([1,3,6], name="a")

        ema2 = ema(3)
        asserted_sr = ema2.getSr(base_sr)
        expected_sr = pd.Series([1,2,4])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            self.assertEqual(expected_sr[i], asserted_sr[i])
        
        self.assertEqual(ema2.expect_name("a"), asserted_sr.name)
        self.assertEqual("EMA3[a]", asserted_sr.name)

    def test_get_sr_name_from_sr_with_tuple(self):
        base_sr = pd.Series([1,3,6], name=("a","1"))

        ema2 = ema(3)
        asserted_sr = ema2.getSr(base_sr)
        expected_sr = pd.Series([1,2,4])

        self.assertEqual(len(asserted_sr),len(expected_sr))

        for i in range(len(asserted_sr)):
            self.assertEqual(expected_sr[i], asserted_sr[i])
        
        self.assertEqual(ema2.expect_name("1"), asserted_sr.name[1])
        self.assertEqual(("a","EMA3[1]"), asserted_sr.name)