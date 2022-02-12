import unittest
import pandas as pd
import numpy as np
from quote_source.client.TimeFrame import TimeFrame
from datetime import datetime
from src.candle_up_time_frame.aggregator import Aggregator        
from pandas import Timestamp       

class MyTestCase(unittest.TestCase):
    def test_condense_single_1(self):
        df = pd.DataFrame(np.array([[1, 10, 3,5 ,10], [5, 9, 2,8,20], [6, 5, 15,1,30]]),
                        columns=["O","H","L", "C","V"], 
                        index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,6)]))
        
        expDf = pd.DataFrame(np.array([[1, 10, 3,5,10], [1, 10, 2,8,30], [6, 5, 15,1,30]]),
                            columns=["O","H","L", "C","V"], 
                            index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,6)]))
            
        tfcs = Aggregator()
        
        condDf = tfcs.aggregate(df, TimeFrame.MINUTE5, False)
        self.assertTrue(expDf.equals(condDf))
        print(expDf)
        print(condDf)
    
    def test_condense_single_2(self):
        df = pd.DataFrame(np.array([[1, 10, 3,5,10], [5, 9, 2,8,20], [3, 7, 1, 3,30], [6, 10, 2,1,40]]),
                        columns=["O","H","L", "C","V"], 
                        index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,5), datetime(2000,1,1,1,6)]))
        
        expDf = pd.DataFrame(np.array([[1, 10, 3,5,10], [1, 10, 2,8,30],[3,7,1,3,30], [3, 10, 1,1,70]]),
                            columns=["O","H","L", "C","V"], 
                            index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,5), datetime(2000,1,1,1,6)]))
             
        tfcs = Aggregator()
        
        condDf = tfcs.aggregate(df, TimeFrame.MINUTE5, False)
        self.assertTrue(expDf.equals(condDf))
        print(expDf)
        print(condDf)

    def test_condense_mass_1(self):
        df = pd.DataFrame(np.array([[1, 10, 3,5,10], [5, 9, 2,8,20], [3, 7, 1, 3,30], [6, 10, 2,1,40]]),
                        columns=["O","H","L", "C","V"], 
                        index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,15), datetime(2000,1,1,1,20)]))


        expDf1 = pd.DataFrame(np.array([[1, 10, 3,5,10], [1, 10, 2,8,30],[3,7,1,3,30], [6, 10, 2,1,40]]),
                            columns=["O","H","L", "C","V"], 
                            index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,15), datetime(2000,1,1,1,20)]))
        
        expDf2 = pd.DataFrame(np.array([[1, 10, 3,5,10], [1, 10, 2,8,30],[3,7,1,3,30], [3, 10, 1,1,70]]),
                            columns=["O","H","L", "C","V"], 
                            index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,15), datetime(2000,1,1,1,20)]))

        tfcs = Aggregator()
        
        condDf_dic = tfcs.aggregate_mass(df, [TimeFrame.MINUTE5, TimeFrame.MINUTE15], False)
        print(TimeFrame.MINUTE5)
        print(expDf1)
        print(condDf_dic[TimeFrame.MINUTE5])
        print(TimeFrame.MINUTE15)
        print(expDf2)
        print(condDf_dic[TimeFrame.MINUTE15])
        self.assertTrue(expDf1.equals(condDf_dic[TimeFrame.MINUTE5]))
        self.assertTrue(expDf2.equals(condDf_dic[TimeFrame.MINUTE15]))
        self.assertEqual(2, len(condDf_dic))
        
class MyTestCaseWithCondenseDT(unittest.TestCase):
    
    def assert_df(self, df1:pd.DataFrame, df2:pd.DataFrame):
        self.assertEqual(len(df1.columns), len(df2.columns))
        self.assertEqual(len(df1.index), len(df2.index))
        
        for idx in df1.index:
            for col in df1:
                self.assertEqual(df1[col][idx], df2[col][idx], f"Not equal col {col} row {idx}")
    
    def test_condense_single_1(self):
        df = pd.DataFrame(np.array([[1, 10, 3,5 ,10], [5, 9, 2,8,20], [6, 5, 15,1,30]]),
                        columns=["O","H","L", "C","V"], 
                        index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,6)]))
        
        # если просим вернуть колонку DT, то дата должна проставляться по верхнему TimeFrame, 
        # т.е. если у базовой свечи DT 2020-01-01 03:00:00 (TF=HOUR), то для TF=DAY DT = 2020-01-01 00:00:00
        # 03:00:00 обнулилось, хотя это первая свеча дня
        expDf = pd.DataFrame(np.array([
                                [Timestamp(2000,1,1,1),1, 10, 3,5,10], 
                                [Timestamp(2000,1,1,1),1, 10, 2,8,30], 
                                [Timestamp(2000,1,1,1,5),6, 5, 15,1,30]]),
                            columns=["DT","O","H","L", "C","V"], 
                            index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,6)]))
            
        tfcs = Aggregator()
        
        condDf = tfcs.aggregate(df, TimeFrame.MINUTE5, True)
        print(expDf)
        print(condDf)
        self.assert_df(condDf,expDf)
    
    def test_condense_single_2(self):
        df = pd.DataFrame(np.array([[1, 10, 3,  5,  10],
                                    [5, 9,  2,  8,  20], 
                                    [3, 7,  1,  3,  30], 
                                    [6, 10, 2,  1,  40]]),
                        columns=[   "O","H","L","C","V"], 
                        index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,5), datetime(2000,1,1,1,6)]))
        
        expDf = pd.DataFrame(np.array([
                                [Timestamp(2000,1,1,1),     1,  10, 3,  5,  10], 
                                [Timestamp(2000,1,1,1),     1,  10, 2,  8,  30],
                                [Timestamp(2000,1,1,1,5),   3,  7,  1,  3,  30], 
                                [Timestamp(2000,1,1,1,5),   3,  10, 1,  1,  70]]),
                            columns=["DT",                  "O","H","L","C","V"], 
                            index=np.array([
                                Timestamp(2000,1,1,1,1), 
                                Timestamp(2000,1,1,1,3), 
                                Timestamp(2000,1,1,1,5), 
                                Timestamp(2000,1,1,1,6)]))
             
        tfcs = Aggregator()
        
        condDf = tfcs.aggregate(df, TimeFrame.MINUTE5, True)
        print("Assert")
        print(expDf)
        print(condDf)
    
        self.assert_df(condDf,expDf)

    def test_condense_mass_1(self):
        df = pd.DataFrame(np.array([[1, 10, 3,5,10], [5, 9, 2,8,20], [3, 7, 1, 3,30], [6, 10, 2,1,40]]),
                        columns=["O","H","L", "C","V"], 
                        index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,15), datetime(2000,1,1,1,20)]))


        expDf1 = pd.DataFrame(np.array([
                                [Timestamp(2000,1,1,1),1, 10, 3,5,10], 
                                [Timestamp(2000,1,1,1),1, 10, 2,8,30],
                                [Timestamp(2000,1,1,1,15),3,7,1,3,30], 
                                [Timestamp(2000,1,1,1,20),6, 10, 2,1,40]]),
                            columns=["DT","O","H","L", "C","V"], 
                            index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,15), datetime(2000,1,1,1,20)]))
        
        expDf2 = pd.DataFrame(np.array([
                                [Timestamp(2000,1,1,1), 1,10,3,5,10],
                                [Timestamp(2000,1,1,1), 1,10,2,8,30],
                                [Timestamp(2000,1,1,1,15),3,7,1,3,30], 
                                [Timestamp(2000,1,1,1,15),3, 10, 1,1,70]]),
                            columns=["DT", "O","H","L", "C","V"], 
                            index=np.array([datetime(2000,1,1,1,1), datetime(2000,1,1,1,3), datetime(2000,1,1,1,15), datetime(2000,1,1,1,20)]))

        tfcs = Aggregator()
        
        condDf_dic = tfcs.aggregate_mass(df, [TimeFrame.MINUTE5, TimeFrame.MINUTE15], True)
        print(TimeFrame.MINUTE5)
        print(expDf1)
        print(condDf_dic[TimeFrame.MINUTE5])
        print(TimeFrame.MINUTE15)
        print(expDf2)
        print(condDf_dic[TimeFrame.MINUTE15])
        self.assert_df(expDf1,condDf_dic[TimeFrame.MINUTE5])        
        self.assert_df(expDf2,condDf_dic[TimeFrame.MINUTE15])
        self.assertEqual(2, len(condDf_dic))

if __name__ == '__main__':
    unittest.main()
    