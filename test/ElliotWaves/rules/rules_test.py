import unittest
import pandas as pd
import logging
from src.ElliotWaves.direction import direction
from src.ElliotWaves.point import point
from src.ElliotWaves.rules.rules import EW2_gt_SW1, EW3_gt_EW1, EW5_gt_EW3, HW3_gt_HW1_or_HW3_gt_HW5

from src.ElliotWaves.wave import wave


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