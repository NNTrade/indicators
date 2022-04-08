import unittest
import pandas as pd
import logging
from src.SMA.ValueFactory import ValueFactory
from src.OneStockIndicator import OneStockIndicator
from src.Tool.ColName import OpenCandleDT as Odt

class SMAValueFactoryTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_if_send_first_value_then_return_same_value(self):
        """
        Check if non strict send first value
        then get same value
        """
        vf = ValueFactory(3)
        osi = OneStockIndicator(vf)
 
        self.assertEqual({'SMA':123},osi.get_next(pd.Series({Odt: 1, "C":123})))
        
    def test_if_send_series_of_value_then_return_correct(self):
        """
        Check if SMA return correct values
        """
        vf = ValueFactory(3)
        osi = OneStockIndicator(vf)
        
        self.assertEqual({'SMA':3},osi.get_next(pd.Series({Odt: 1,"C":3})))
        self.assertEqual({'SMA':1},osi.get_next(pd.Series({Odt: 1,"C":1})))
        
        self.assertEqual({'SMA':2},osi.get_next(pd.Series({Odt: 2,"C":3})))
        self.assertEqual({'SMA':3},osi.get_next(pd.Series({Odt: 2,"C":5})))
        
        self.assertEqual({'SMA':3},osi.get_next(pd.Series({Odt: 3,"C":3})))
        self.assertEqual({'SMA':4},osi.get_next(pd.Series({Odt: 3,"C":6})))
        
    def test_if_strict_send_series_of_value_then_return_none_until_all_correct(self):
        """
        Check if set property to strict
        then you get None response
        until all periods will be field
        """
        vf = ValueFactory(3, True)
        osi = OneStockIndicator(vf)
        
        self.assertEqual({'SMA':None},osi.get_next(pd.Series({Odt: 1,"C":3})))
        self.assertEqual({'SMA':None},osi.get_next(pd.Series({Odt: 1,"C":1})))
        
        self.assertEqual({'SMA':None},osi.get_next(pd.Series({Odt: 2,"C":3})))
        self.assertEqual({'SMA':None},osi.get_next(pd.Series({Odt: 2,"C":5})))
        
        self.assertEqual({'SMA':3},osi.get_next(pd.Series({Odt: 3,"C":3})))
        self.assertEqual({'SMA':4},osi.get_next(pd.Series({Odt: 3,"C":6})))
        