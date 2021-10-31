import unittest
import pandas as pd
import logging
from .testEnum import TimeFrame
from src.RelativePercent.Factory import PercentFactory

class PercentFactroyTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_percent_calculation(self):
        sr1 = pd.Series([2,1,0,4.5,3])
        sr2 = pd.Series([1,2,3,3,4])        

        pc = PercentFactory()
        asserted_sr = pc.get(sr1,sr2)
        expected_sr = pd.Series([100,-50, -100, 50, -25],name="expected_sr")

        self.logger.debug(asserted_sr)
        self.logger.debug(expected_sr)
        self.assertEqual(len(expected_sr), len(asserted_sr))

        for i in range(len(expected_sr)):
            self.assertEqual(asserted_sr[i], expected_sr[i])
    
    def test_percent_calculation_2_abs(self):
        sr1 = pd.Series([2,1,0,4.5,3])
        sr2 = pd.Series([1,2,3,3,4])        

        pc = PercentFactory(use_abs=True)
        asserted_sr = pc.get(sr1,sr2)
        expected_sr = pd.Series([100,50, 100, 50, 25],name="expected_sr")

        self.logger.debug(asserted_sr)
        self.logger.debug(expected_sr)
        self.assertEqual(len(expected_sr), len(asserted_sr))

        for i in range(len(expected_sr)):
            self.assertEqual(asserted_sr[i], expected_sr[i])
    
    def test_percent_calculation_name(self):
        sr1 = pd.Series([2,1,0,4.5,3],name="b")
        sr2 = pd.Series([1,2,3,3,4],name="ab")        

        pc = PercentFactory()
        asserted_name = pc.get(sr1,sr2).name
        expected_name = "P[b-ab]"

        self.assertEqual(expected_name, asserted_name)
    
    def test_percent_calculation_name_from_tuple(self):
        sr1 = pd.Series([2,1,0,4.5,3],name=("b", "2"))
        sr2 = pd.Series([1,2,3,3,4],name=("a", "1"))

        pc = PercentFactory()
        asserted_name = pc.get(sr1,sr2).name
        expected_name = "P[(b,2)-(a,1)]"

        self.assertEqual(expected_name, asserted_name)

    def test_percent_calculation_name_from_tuple_TimeFrame(self):
        sr1 = pd.Series([2,1,0,4.5,3],name=(TimeFrame.HOURLY, "2"))
        sr2 = pd.Series([1,2,3,3,4],name=(TimeFrame.MINUTES15, "1"))        

        pc = PercentFactory()
        asserted_name = pc.get(sr1,sr2).name
        expected_name = f"P[(H,2)-(m15,1)]"

        self.assertEqual(expected_name, asserted_name)

    def test_percent_calculation_between(self):
        sr1_1 = pd.Series([1,3], name="sr1_1")
        sr1_2 = pd.Series([2,6], name="sr1_2")
        df1 = pd.concat([sr1_1, sr1_2],axis=1)

        sr2_1 = pd.Series([6,3],  name="sr2_1")
        sr2_2 = pd.Series([8,12],  name="sr2_2")   
        sr2_3 = pd.Series([10,0], name="sr2_3")   
        df2 = pd.concat([sr2_1, sr2_2, sr2_3],axis=1)

        pc = PercentFactory()
        asserted_df = pc.get_between_df(df2,df1)
        expected_df = pd.concat([
                pd.Series([500,0],name="P[sr2_1-sr1_1]"),
                pd.Series([700,300],name="P[sr2_2-sr1_1]"),
                pd.Series([900,-100],name="P[sr2_3-sr1_1]"),

                pd.Series([200,-50],name="P[sr2_1-sr1_2]"),
                pd.Series([300,100],name="P[sr2_2-sr1_2]"),
                pd.Series([400,-100],name="P[sr2_3-sr1_2]")
            ],axis=1)

        self.logger.debug(asserted_df)
        self.logger.debug(expected_df)
        self.assertEqual(len(expected_df.columns), len(asserted_df.columns))
        self.assertEqual(len(expected_df.index), len(asserted_df.index))

        for c in expected_df.columns:
            for i in range(len(expected_df.index)):
                self.assertEqual(asserted_df[c][i], expected_df[c][i], msg=f"Error in col {c} in index {i}")



    def test_percent_calculation_all(self):
        sr3 = pd.Series([1,3], name="sr1")
        sr2 = pd.Series([2,4], name="sr2")
        sr1 = pd.Series([5,4], name="sr3")
        df = pd.concat([sr1, sr2, sr3],axis=1)

        pc = PercentFactory()
        asserted_df = pc.get_for_all_df(df)
        expected_df = pd.concat([
                pd.Series([-50,-25],name="P[sr1-sr2]"),
                pd.Series([-80,-25],name="P[sr1-sr3]"),

                pd.Series([-60,0],name="P[sr2-sr3]")
            ],axis=1)

        self.logger.debug(asserted_df)
        self.logger.debug(expected_df)
        self.assertEqual(len(expected_df.columns), len(asserted_df.columns))
        self.assertEqual(len(expected_df.index), len(asserted_df.index))

        for c in expected_df.columns:
            for i in range(len(expected_df.index)):
                self.assertEqual(asserted_df[c][i], expected_df[c][i], msg=f"Error in col {c} in index {i}")

  
