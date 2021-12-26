import unittest
import pandas as pd
import logging
from src.ElliotWaves.misc.direction import direction
from src.ElliotWaves.misc.point import point
from src.ElliotWaves.rules.rules import EW2_gt_SW1, EW3_gt_EW1, EW5_gt_EW3, \
                                        EWx_SWx_is_ext_RWx, HW3_gt_HW1_or_HW3_gt_HW5, \
                                        HWx_gt_HWy_and_HWx_gt_HWz, TWx_not_TWy_not_TWz, \
                                        W2_dif_W4, EW4_gt_EW1

from src.ElliotWaves.misc.wave import wave
from src.ElliotWaves.misc.type import type


class EW2_gt_SW1_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    dt_sw1 = pd.Timestamp.today()
    dt_ew1 = pd.Timestamp.today() + pd.Timedelta(days = 1)
    dt_sw2 = pd.Timestamp.today() + pd.Timedelta(days = 1)
    dt_ew2 = pd.Timestamp.today() + pd.Timedelta(days = 2)       

    def test_EW2_gt_SW1__Success(self):
        wave1 = wave(point(self.dt_sw1, 1.1),point(self.dt_ew1, 1.2))
        wave2 = wave(point(self.dt_sw2, 1.2),point(self.dt_ew2, 1.15))
        self.assertTrue(EW2_gt_SW1(wave1,wave2, direction.Long))

    def test_EW2_eq_SW1__Fail(self):
        wave1 = wave(point(self.dt_sw1, 1.1),point(self.dt_ew1, 1.2))
        wave2 = wave(point(self.dt_sw2, 1.2),point(self.dt_ew2, 1.1))
        self.assertFalse(EW2_gt_SW1(wave1,wave2, direction.Long))

    def test_EW2_ls_SW1__Fail(self):
        wave1 = wave(point(self.dt_sw1, 1.1),point(self.dt_ew1, 1.2))
        wave2 = wave(point(self.dt_sw2, 1.2),point(self.dt_ew2, 1))
        self.assertFalse(EW2_gt_SW1(wave1,wave2, direction.Long))

    def test_short_dir_EW2_ls_SW1__Success(self):
        wave1 = wave(point(self.dt_sw1, 1.2),point(self.dt_ew1, 1.1))
        wave2 = wave(point(self.dt_sw2, 1.1),point(self.dt_ew2, 1.15))
        self.assertTrue(EW2_gt_SW1(wave1,wave2, direction.Short))

    def test_short_dir_EW2_eq_SW1__Fail(self):
        wave1 = wave(point(self.dt_sw1, 1.2),point(self.dt_ew1, 1.1))
        wave2 = wave(point(self.dt_sw2, 1.1),point(self.dt_ew2, 1.2))
        self.assertFalse(EW2_gt_SW1(wave1,wave2, direction.Short))
        
    def test_short_dir_EW2_gt_SW1__Fail(self):
        wave1 = wave(point(self.dt_sw1, 1.2),point(self.dt_ew1, 1.1))
        wave2 = wave(point(self.dt_sw2, 1.1),point(self.dt_ew2, 1.3))
        self.assertFalse(EW2_gt_SW1(wave1,wave2, direction.Short))

class EW3_gt_EW1_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    dt_sw1 = pd.Timestamp.today()
    dt_ew1 = pd.Timestamp.today() + pd.Timedelta(days = 1)
    dt_sw3 = pd.Timestamp.today() + pd.Timedelta(days = 2)
    dt_ew3 = pd.Timestamp.today() + pd.Timedelta(days = 3)    

    def test_EW3_gt_EW1__success(self):
        wave1 = wave(point(self.dt_sw1, 1.1),point(self.dt_ew1, 1.2))
        wave3 = wave(point(self.dt_sw3, 1.15),point(self.dt_ew3, 1.3))

        self.assertTrue(EW3_gt_EW1(wave1,wave3, direction.Long))

    def test_EW3_eq_EW1__fail(self):
        wave1 = wave(point(self.dt_sw1, 1.1),point(self.dt_ew1, 1.2))
        wave3 = wave(point(self.dt_sw3, 1.15),point(self.dt_ew3, 1.2))

        self.assertFalse(EW3_gt_EW1(wave1,wave3, direction.Long))
    def test_EW3_ls_EW1__fail(self):
        wave1 = wave(point(self.dt_sw1, 1.1),point(self.dt_ew1, 1.2))
        wave3 = wave(point(self.dt_sw3, 1.15),point(self.dt_ew3, 1.18))

        self.assertFalse(EW3_gt_EW1(wave1,wave3, direction.Long))

    def test_short_dir_EW3_ls_EW1__success(self):
        wave1 = wave(point(self.dt_sw1, 1.2),point(self.dt_ew1, 1.1))
        wave3 = wave(point(self.dt_sw3, 1.15),point(self.dt_ew3, 1.05))

        self.assertTrue(EW3_gt_EW1(wave1,wave3, direction.Short))
    def test_short_dir_EW3_eq_EW1__fail(self):
        wave1 = wave(point(self.dt_sw1, 1.2),point(self.dt_ew1, 1.1))
        wave3 = wave(point(self.dt_sw3, 1.15),point(self.dt_ew3, 1.1))

        self.assertFalse(EW3_gt_EW1(wave1,wave3, direction.Short))
    def test_short_dir_EW3_gt_EW1__fail(self):
        wave1 = wave(point(self.dt_sw1, 1.2),point(self.dt_ew1, 1.1))
        wave3 = wave(point(self.dt_sw3, 1.15),point(self.dt_ew3, 1.13))

        self.assertFalse(EW3_gt_EW1(wave1,wave3, direction.Short))

class HW3_gt_HW1_or_HW3_gt_HW5_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    dt_sw1 = pd.Timestamp.today()
    dt_ew1 = pd.Timestamp.today() + pd.Timedelta(days = 1)
    dt_sw3 = pd.Timestamp.today() + pd.Timedelta(days = 2)
    dt_ew3 = pd.Timestamp.today() + pd.Timedelta(days = 3) 
    dt_sw5 = pd.Timestamp.today() + pd.Timedelta(days = 4)
    dt_ew5 = pd.Timestamp.today() + pd.Timedelta(days = 5)

    def test_HW3_gt_HW1__success(self):
        wave1 = wave(point(self.dt_sw1, 1.1),point(self.dt_ew1, 1.2))
        wave3 = wave(point(self.dt_sw3, 1.15),point(self.dt_ew3, 1.3))
        wave5 = wave(point(self.dt_sw3, 2.2),point(self.dt_ew3, 3.3))

        self.assertTrue(HW3_gt_HW1_or_HW3_gt_HW5(wave1,wave3,wave5))

    def test_HW3_gt_HW5__success(self):
        wave1 = wave(point(self.dt_sw1, 1.1),point(self.dt_ew1, 2.2))
        wave3 = wave(point(self.dt_sw3, 2.15),point(self.dt_ew3, 2.3))
        wave5 = wave(point(self.dt_sw3, 2.2),point(self.dt_ew3, 2.3))

        self.assertTrue(HW3_gt_HW1_or_HW3_gt_HW5(wave1,wave3,wave5))

    def test_HW3_gt_HW5_and_HW3_gt_HW5__success(self):
        wave1 = wave(point(self.dt_sw1, 1.1),point(self.dt_ew1, 1.2))
        wave3 = wave(point(self.dt_sw3, 1.15),point(self.dt_ew3, 2.3))
        wave5 = wave(point(self.dt_sw3, 2.2),point(self.dt_ew3, 2.3))

        self.assertTrue(HW3_gt_HW1_or_HW3_gt_HW5(wave1,wave3,wave5))

    def test_HW3_eq_HW5_and_HW3_eq_HW3__fail(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 3))
        wave3 = wave(point(self.dt_sw3, 2),point(self.dt_ew3, 4))
        wave5 = wave(point(self.dt_sw3, 3),point(self.dt_ew3, 5))

        self.assertFalse(HW3_gt_HW1_or_HW3_gt_HW5(wave1,wave3,wave5))

    def test_HW3_ls_HW5_and_HW3_ls_HW3__fail(self):
        wave1 = wave(point(self.dt_sw1, 1.1),point(self.dt_ew1, 2.2))
        wave3 = wave(point(self.dt_sw3, 2.15),point(self.dt_ew3, 2.25))
        wave5 = wave(point(self.dt_sw3, 2.2),point(self.dt_ew3, 3.3))

        self.assertFalse(HW3_gt_HW1_or_HW3_gt_HW5(wave1,wave3,wave5))

class EW4_gt_EW1_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    dt_sw1 = pd.Timestamp.today() + pd.Timedelta(days = 2)
    dt_ew1 = pd.Timestamp.today() + pd.Timedelta(days = 3) 
    dt_sw4 = pd.Timestamp.today() + pd.Timedelta(days = 4)
    dt_ew4 = pd.Timestamp.today() + pd.Timedelta(days = 5)

    def test_EW4_gt_EW1__success(self):
        wave1 = wave(point(self.dt_sw1, 2),point(self.dt_ew1, 4))
        wave4 = wave(point(self.dt_sw4, 3),point(self.dt_ew4, 5))

        self.assertTrue(EW4_gt_EW1(wave1,wave4, direction.Long))
    def test_EW4_eq_EW1__fail(self):
        wave1 = wave(point(self.dt_sw1, 2),point(self.dt_ew1, 4))
        wave4 = wave(point(self.dt_sw4, 3),point(self.dt_ew4, 4))

        self.assertFalse(EW4_gt_EW1(wave1,wave4, direction.Long))
    def test_EW4_ls_EW1__fail(self):
        wave1 = wave(point(self.dt_sw1, 2),point(self.dt_ew1, 4))
        wave4 = wave(point(self.dt_sw4, 3),point(self.dt_ew4, 3.8))

        self.assertFalse(EW4_gt_EW1(wave1,wave4, direction.Long))  

    def test_short_dir_EW4_ls_EW1__success(self):
        wave1 = wave(point(self.dt_sw1, 4),point(self.dt_ew1, 2))
        wave4 = wave(point(self.dt_sw4, 3),point(self.dt_ew4, 1))

        self.assertTrue(EW4_gt_EW1(wave1,wave4, direction.Short))
    def test_short_dir_EW4_eq_EW1__fail(self):
        wave1 = wave(point(self.dt_sw1, 4),point(self.dt_ew1, 2))
        wave4 = wave(point(self.dt_sw4, 3),point(self.dt_ew4, 2))

        self.assertFalse(EW4_gt_EW1(wave1,wave4, direction.Short))
    def test_short_dir_EW4_gt_EW1__fail(self):
        wave1 = wave(point(self.dt_sw1, 4),point(self.dt_ew1, 2))
        wave4 = wave(point(self.dt_sw4, 3),point(self.dt_ew4, 2.8))

        self.assertFalse(EW4_gt_EW1(wave1,wave4, direction.Short))

class EW5_gt_EW3_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    dt_sw3 = pd.Timestamp.today() + pd.Timedelta(days = 2)
    dt_ew3 = pd.Timestamp.today() + pd.Timedelta(days = 3) 
    dt_sw5 = pd.Timestamp.today() + pd.Timedelta(days = 4)
    dt_ew5 = pd.Timestamp.today() + pd.Timedelta(days = 5)

    def test_EW5_gt_EW3__success(self):
        wave3 = wave(point(self.dt_sw3, 2),point(self.dt_ew3, 4))
        wave5 = wave(point(self.dt_sw5, 3),point(self.dt_ew5, 5))

        self.assertTrue(EW5_gt_EW3(wave3,wave5, direction.Long))
    def test_EW5_eq_EW3__fail(self):
        wave3 = wave(point(self.dt_sw3, 2),point(self.dt_ew3, 4))
        wave5 = wave(point(self.dt_sw5, 3),point(self.dt_ew5, 4))

        self.assertFalse(EW5_gt_EW3(wave3,wave5, direction.Long))
    def test_EW5_ls_EW3__fail(self):
        wave3 = wave(point(self.dt_sw3, 2),point(self.dt_ew3, 4))
        wave5 = wave(point(self.dt_sw5, 3),point(self.dt_ew5, 3.8))

        self.assertFalse(EW5_gt_EW3(wave3,wave5, direction.Long))  

    def test_short_dir_EW5_ls_EW3__success(self):
        wave3 = wave(point(self.dt_sw3, 4),point(self.dt_ew3, 2))
        wave5 = wave(point(self.dt_sw5, 3),point(self.dt_ew5, 1))

        self.assertTrue(EW5_gt_EW3(wave3,wave5, direction.Short))
    def test_short_dir_EW5_eq_EW3__fail(self):
        wave3 = wave(point(self.dt_sw3, 4),point(self.dt_ew3, 2))
        wave5 = wave(point(self.dt_sw5, 3),point(self.dt_ew5, 2))

        self.assertFalse(EW5_gt_EW3(wave3,wave5, direction.Short))
    def test_short_dir_EW5_gt_EW3__fail(self):
        wave3 = wave(point(self.dt_sw3, 4),point(self.dt_ew3, 2))
        wave5 = wave(point(self.dt_sw5, 3),point(self.dt_ew5, 2.8))

        self.assertFalse(EW5_gt_EW3(wave3,wave5, direction.Short))

class W2_dif_W4_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    dt_sw2 = pd.Timestamp.today() + pd.Timedelta(days = 2)
    dt_ew2 = pd.Timestamp.today() + pd.Timedelta(days = 3) 
    dt_sw4 = pd.Timestamp.today() + pd.Timedelta(days = 4)
    dt_ew4 = pd.Timestamp.today() + pd.Timedelta(days = 5)


    def test_W2_dif_height_W4__succes(self):
        wave2 = wave(point(self.dt_sw2, 4),point(self.dt_ew2, 2))
        wave4 = wave(point(self.dt_sw4, 5),point(self.dt_ew4, 4))

        self.assertTrue(W2_dif_W4(wave2,wave4))
    def test_W2_dif_time_W4__succes(self):
        wave2 = wave(point(self.dt_sw2, 4),point(self.dt_ew2, 2))
        wave4 = wave(point(self.dt_sw4, 5),point(self.dt_ew4 + pd.Timedelta(days = 1), 3))

        self.assertTrue(W2_dif_W4(wave2,wave4))
    def test_W2_dif_type_W4__succes(self):
        wave2 = wave(point(self.dt_sw2, 4),point(self.dt_ew2, 2))
        wave4 = wave(point(self.dt_sw4, 5),point(self.dt_ew4, 3),type.not_implemented_for_test)

        self.assertTrue(W2_dif_W4(wave2,wave4))
    
    
    def test_W2_dif_height_time_W4__succes(self):
        wave2 = wave(point(self.dt_sw2, 4),point(self.dt_ew2 + pd.Timedelta(days = 1), 2))
        wave4 = wave(point(self.dt_sw4, 5),point(self.dt_ew4, 4))

        self.assertTrue(W2_dif_W4(wave2,wave4))
    def test_W2_dif_time_type_W4__succes(self):
        wave2 = wave(point(self.dt_sw2, 4),point(self.dt_ew2, 2),type.not_implemented_for_test)
        wave4 = wave(point(self.dt_sw4 + pd.Timedelta(days = 1), 5),point(self.dt_ew4, 3))

        self.assertTrue(W2_dif_W4(wave2,wave4))
    def test_W2_dif_height_type_W4__succes(self):
        wave2 = wave(point(self.dt_sw2, 4),point(self.dt_ew2, 1))
        wave4 = wave(point(self.dt_sw4, 5),point(self.dt_ew4, 3),type.not_implemented_for_test)

        self.assertTrue(W2_dif_W4(wave2,wave4))
    
    
    def test_W2_dif_height_time_type_W4__succes(self):
        wave2 = wave(point(self.dt_sw2, 4),point(self.dt_ew2 + pd.Timedelta(seconds = 1), 2))
        wave4 = wave(point(self.dt_sw4, 6),point(self.dt_ew4, 3),type.not_implemented_for_test)

        self.assertTrue(W2_dif_W4(wave2,wave4))


    def test_W2_no_dif_W4__fail(self):
        wave2 = wave(point(self.dt_sw2, 4),point(self.dt_ew2, 2))
        wave4 = wave(point(self.dt_sw4, 5),point(self.dt_ew4, 3))

        self.assertFalse(W2_dif_W4(wave2,wave4))

class HWx_gt_HWy_and_HWx_gt_HWz_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)


    dt_sw1 = pd.Timestamp.today()
    dt_ew1 = pd.Timestamp.today() + pd.Timedelta(days = 1)
    dt_sw3 = pd.Timestamp.today() + pd.Timedelta(days = 2)
    dt_ew3 = pd.Timestamp.today() + pd.Timedelta(days = 3) 
    dt_sw5 = pd.Timestamp.today() + pd.Timedelta(days = 4)
    dt_ew5 = pd.Timestamp.today() + pd.Timedelta(days = 5)

    def test_HW5_gt_than_other__success(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 3)) 
        wave3 = wave(point(self.dt_sw3, 2),point(self.dt_ew3, 4)) 
        wave5 = wave(point(self.dt_sw3, 5),point(self.dt_ew3, 8.1))

        self.assertTrue(HWx_gt_HWy_and_HWx_gt_HWz(wave1,wave3,wave5,0.5))
    
    def test_HW5_not_gt_than_other__success(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 3)) 
        wave3 = wave(point(self.dt_sw3, 2),point(self.dt_ew3, 4)) 
        wave5 = wave(point(self.dt_sw3, 5),point(self.dt_ew3, 7.9)) 

        self.assertFalse(HWx_gt_HWy_and_HWx_gt_HWz(wave1,wave3,wave5,0.5))

    def test_HW3_gt_than_other__success(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 3)) 
        wave3 = wave(point(self.dt_sw3, 2),point(self.dt_ew3, 5.1)) 
        wave5 = wave(point(self.dt_sw3, 5),point(self.dt_ew3, 7)) 

        self.assertTrue(HWx_gt_HWy_and_HWx_gt_HWz(wave1,wave3,wave5,0.5))
    
    def test_HW5_not_gt_than_other__success(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 3)) 
        wave3 = wave(point(self.dt_sw3, 2),point(self.dt_ew3, 4.9)) 
        wave5 = wave(point(self.dt_sw3, 5),point(self.dt_ew3, 7)) 

        self.assertFalse(HWx_gt_HWy_and_HWx_gt_HWz(wave1,wave3,wave5,0.5))


    def test_HW1_and_HW5_gt_than_HW1__fail(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 3)) 
        wave3 = wave(point(self.dt_sw3, 2),point(self.dt_ew3, 5.1)) 
        wave5 = wave(point(self.dt_sw3, 5),point(self.dt_ew3, 8.1)) 

        self.assertFalse(HWx_gt_HWy_and_HWx_gt_HWz(wave1,wave3,wave5,0.5))

    def test_all_equeal__fail(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 3)) 
        wave3 = wave(point(self.dt_sw3, 2),point(self.dt_ew3, 4)) 
        wave5 = wave(point(self.dt_sw3, 5),point(self.dt_ew3, 7))

        self.assertFalse(HWx_gt_HWy_and_HWx_gt_HWz(wave1,wave3,wave5,0.01))

class TWx_not_TWy_not_TWz_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_TW3_gt_than_TW1__success(self):
        dt_sw1 = pd.Timestamp.today()
        dt_ew1 = dt_sw1 + pd.Timedelta(days = 1)
        dt_sw2 = dt_ew1
        dt_ew2 = dt_sw2 + pd.Timedelta(days = 2) 
        dt_sw3 = dt_ew2
        dt_ew3 = dt_sw3 + pd.Timedelta(days = 4)

        wave1 = wave(point(dt_sw1, 1),point(dt_ew1, 3)) 
        wave2 = wave(point(dt_sw2, 2),point(dt_ew2, 4)) 
        wave3 = wave(point(dt_sw3, 5),point(dt_ew3, 7))

        self.assertTrue(TWx_not_TWy_not_TWz([wave1,wave2, wave3], dif_percent=0.5))
    
    def test_TW3_not_gt_than_TW1__fail(self):
        dt_sw1 = pd.Timestamp.today()
        dt_ew1 = dt_sw1 + pd.Timedelta(days = 1)
        dt_sw2 = dt_ew1
        dt_ew2 = dt_sw2 + pd.Timedelta(days = 2) 
        dt_sw3 = dt_ew2
        dt_ew3 = dt_sw3 + pd.Timedelta(days = 4)

        wave1 = wave(point(dt_sw1, 1),point(dt_ew1, 3)) 
        wave2 = wave(point(dt_sw2, 2),point(dt_ew2, 4)) 
        wave3 = wave(point(dt_sw3, 5),point(dt_ew3, 7))

        self.assertFalse(TWx_not_TWy_not_TWz([wave1,wave2, wave3], dif_percent=1.01))

    def test_array_too_small__exception(self):
        dt_sw1 = pd.Timestamp.today()
        dt_ew1 = pd.Timestamp.today() + pd.Timedelta(days = 1)
        dt_sw2 = pd.Timestamp.today() + pd.Timedelta(days = 1)
        dt_ew2 = pd.Timestamp.today() + pd.Timedelta(days = 10) 

        wave1 = wave(point(dt_sw1, 1),point(dt_ew1, 3)) 
        wave2 = wave(point(dt_sw2, 2),point(dt_ew2, 4)) 
        
        with self.assertRaises(Exception):
            TWx_not_TWy_not_TWz([wave1,wave2], dif_percent=1)

    def test_array_too_big__exception(self):
        dt_sw1 = pd.Timestamp.today()
        dt_ew1 = pd.Timestamp.today() + pd.Timedelta(days = 1)
        dt_sw2 = pd.Timestamp.today() + pd.Timedelta(days = 1)
        dt_ew2 = pd.Timestamp.today() + pd.Timedelta(days = 10) 
        dt_sw3 = pd.Timestamp.today() + pd.Timedelta(days = 2)
        dt_ew3 = pd.Timestamp.today() + pd.Timedelta(days = 4)
        dt_sw4 = pd.Timestamp.today() + pd.Timedelta(days = 2)
        dt_ew4 = pd.Timestamp.today() + pd.Timedelta(days = 4)

        wave1 = wave(point(dt_sw1, 1),point(dt_ew1, 3)) 
        wave2 = wave(point(dt_sw2, 2),point(dt_ew2, 4)) 
        wave3 = wave(point(dt_sw3, 2),point(dt_ew3, 4)) 
        wave4 = wave(point(dt_sw4, 2),point(dt_ew4, 4)) 
        
        with self.assertRaises(Exception):
            TWx_not_TWy_not_TWz([wave1,wave2,wave3,wave4], dif_percent=1)

class EWx_SWx_is_ext_RWx_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)
    
    dt_sw1 = pd.Timestamp.today()
    dt_ew1 = pd.Timestamp.today() + pd.Timedelta(days = 1)

    def test_is_ext__success(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 10)) 
        df = pd.DataFrame(data={"H":[3,5,7,10], "L":[1,3,5,7]})

        self.assertTrue(EWx_SWx_is_ext_RWx(wave1, df))
    
    def test_is_ext_for_short_dir__success(self):
        wave1 = wave(point(self.dt_sw1, 10),point(self.dt_ew1, 1)) 
        df = pd.DataFrame(data={"H":[10,7,5,3], "L":[7,5,3,1]})

        self.assertTrue(EWx_SWx_is_ext_RWx(wave1, df))
    
    def test_is_not_ext_by_High__fail(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 10)) 
        df = pd.DataFrame(data={"H":[3,15,7,10], "L":[1,3,5,7]})

        self.assertFalse(EWx_SWx_is_ext_RWx(wave1, df))
    
    def test_is_not_ext_by_Low__fail(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 10)) 
        df = pd.DataFrame(data={"H":[3,5,7,10], "L":[1,3,0.4,7]})

        self.assertFalse(EWx_SWx_is_ext_RWx(wave1, df))

    def test_for_long_end_checked_by_H__success(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 10)) 
        df = pd.DataFrame(data={"H":[3,5,7,10], "L":[1,3,100,7]})

        self.assertTrue(EWx_SWx_is_ext_RWx(wave1, df))
    
    def test_for_long_start_checked_by_L__success(self):
        wave1 = wave(point(self.dt_sw1, 1),point(self.dt_ew1, 10)) 
        df = pd.DataFrame(data={"H":[3,5,0.7,10], "L":[1,3,5,7]})

        self.assertTrue(EWx_SWx_is_ext_RWx(wave1, df))
    
    def test_for_stort_end_checked_by_L__success(self):
        wave1 = wave(point(self.dt_sw1, 10),point(self.dt_ew1, 1)) 
        df = pd.DataFrame(data={"H":[10,7,0.5,3], "L":[7,5,3,1]})

        self.assertTrue(EWx_SWx_is_ext_RWx(wave1, df))
    
    def test_for_stort_start_checked_by_H__success(self):
        wave1 = wave(point(self.dt_sw1, 10),point(self.dt_ew1, 1)) 
        df = pd.DataFrame(data={"H":[10,7,5,3], "L":[7,5,13,1]})

        self.assertTrue(EWx_SWx_is_ext_RWx(wave1, df))