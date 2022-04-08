import logging
from typing import Dict, List, Tuple
import unittest
import pandas as pd
from src.OneStockIndicator import OneStockIndicator, Odt
from src.BaseIndicatorCalculator import BaseIndicatorCalculator

class Indicator(BaseIndicatorCalculator):
    def calc_value(self, series: pd.Series, state: Dict) -> Tuple[Dict[str, float], Dict]:
        if (len(state) == 0):
            return {"t":1}, {f'C{series[Odt]}':1}
        else:
            state[f'C{series[Odt]}'] = 1
            return {"t":2}, state.copy()

class ChenarioIndicator(BaseIndicatorCalculator):
    
    @staticmethod
    def get_candles()->List[pd.Series]:
        exp_candles = []
        exp_candles.append(pd.Series({Odt:1, "V":1}))
        exp_candles.append(pd.Series({Odt:1, "V":2}))
        exp_candles.append(pd.Series({Odt:2, "V":3}))
        exp_candles.append(pd.Series({Odt:2, "V":4}))
        exp_candles.append(pd.Series({Odt:3, "V":5}))
        exp_candles.append(pd.Series({Odt:3, "V":6}))
        return exp_candles
    
    @staticmethod
    def get_values()->List:
        values = []
        values.append({"Val":1})
        values.append({"Val":2})
        values.append({"Val":3})
        values.append({"Val":4})
        values.append({"Val":5})
        values.append({"Val":6})
        return values
            
    def __init__(self):
        self.exp_candles = ChenarioIndicator.get_candles()
        
        self.states = []
        self.states.append({"St":1})
        self.states.append({"St":2})
        self.states.append({"St":3})
        self.states.append({"St":4})
        self.states.append({"St":5})
        self.states.append({"St":6})
        
        self.exp_states = []
        self.exp_states.append({})
        self.exp_states.append({})
        self.exp_states.append({"St":2})
        self.exp_states.append({"St":2})
        self.exp_states.append({"St":4})
        self.exp_states.append({"St":4})
        
        self.values = ChenarioIndicator.get_values()
        
    def calc_value(self, candle: pd.Series, state: Dict) -> Tuple[Dict[str, float], Dict]:
        exp_state : Dict = self.exp_states.pop(0)
        exp_candle : pd.Series = self.exp_candles.pop(0)
        
        if (exp_candle.equals(candle) != True):
            raise Exception(f'Wrong Candle exp: {exp_candle} get {candle}')
        
        if (exp_state != state):
            raise Exception(f'Wrong State exp: {exp_state} get {state}')
        
        return self.values.pop(0), self.states.pop(0)


class OneStockIndicatorTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)
    
    def test_if_send_first_candle_return_first_calc_and_state(self):
        
        osi = OneStockIndicator(Indicator())
        expected_resp = {"t":1}
        expected_state = {f'C1':1}
        
        asserted_resp = osi.get_next(pd.Series({Odt: 1}))
        asserted_state = osi.get_state()
        
        self.assertEqual(expected_resp,asserted_resp)
        self.assertEqual(expected_state,asserted_state)
        
    def test_if_send_first_candle_several_time_return_first_calc_and_state(self):
        
        osi = OneStockIndicator(Indicator())
        expected_resp = {"t":1}
        expected_state = {f'C1':1}
        
        osi.get_next(pd.Series({Odt: 1}))
        asserted_resp = osi.get_next(pd.Series({Odt: 1}))
        asserted_state = osi.get_state()
        
        self.assertEqual(expected_resp,asserted_resp)
        self.assertEqual(expected_state,asserted_state)
        
    def test_if_send_second_candle_return_second_calc_and_state(self):
        
        osi = OneStockIndicator(Indicator())
        expected_resp = {"t":2}
        expected_state = {f'C1':1, f'C2':1}
        
        osi.get_next(pd.Series({Odt: 1}))
        asserted_resp = osi.get_next(pd.Series({Odt: 2}))
        asserted_state = osi.get_state()
        
        self.assertEqual(expected_resp,asserted_resp)
        self.assertEqual(expected_state,asserted_state)
        
        
    def test_schenario(self):
        ci = ChenarioIndicator()
        osi = OneStockIndicator(ci)
        candles = ChenarioIndicator.get_candles()
        expect_values = ChenarioIndicator.get_values()
        
        for i in range(len(candles)):
            candle = candles.pop(0)
            expect_value = expect_values.pop(0)
            assert_value = osi.get_next(candle)
            self.assertEqual(expect_value, assert_value)    
        
        self.assertEqual(0, len(candles))
        self.assertEqual(0, len(expect_values))
        

        
        