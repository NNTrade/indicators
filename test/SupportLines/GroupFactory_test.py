import unittest
import pandas as pd
import logging
from src.SupportLines.GroupFactory import split_by_count, split_by_interval,classify_price_sr_by_group,group_col_name

class SplitByCountTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_border_is_correct(self):
        min = 1
        max = 5
        count = 13

        asserted_tpl = split_by_count(min, max,count)

        self.assertEqual(5,asserted_tpl[1]["Till"].iloc[len(asserted_tpl[1])-1])
        self.assertEqual(1,asserted_tpl[1]["From"].iloc[0])

    def test_count_amount(self):
        min = 1
        max = 5
        count = 13

        asserted_tpl = split_by_count(min, max,count)

        self.assertEqual(count,len(asserted_tpl[1]))
    
    def test_no_borders_out_of_range(self):
        min = 1
        max = 5
        count = 13

        asserted_tpl = split_by_count(min, max,count)

        self.assertTrue(asserted_tpl[1]["From"].min() == min)
        self.assertTrue(asserted_tpl[1]["Till"].max() == max)

    def test_check_group(self):
        min = 1
        max = 5
        count = 13

        asserted_tpl = split_by_count(min, max,count)

        fr = min
        for index, row in asserted_tpl[1].iterrows():
            self.assertEqual(fr, row["From"])
            self.assertTrue(row["Till"]>row["From"])
            fr = row["Till"]
        self.assertEqual(max,fr)

class SplitByIntervalTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_border_is_correct(self):
        min = 1
        max = 5
        interval = 0.66

        asserted_tpl = split_by_interval(min, max,interval)

        self.assertEqual(5,asserted_tpl[1]["Till"].iloc[len(asserted_tpl[1])-1])
        self.assertEqual(1,asserted_tpl[1]["From"].iloc[0])

    def test_count_amount(self):
        min = 1
        max = 5
        interval = 0.5

        asserted_tpl = split_by_interval(min, max,interval)

        self.assertEqual(8,len(asserted_tpl[1]))
    
    def test_no_borders_out_of_range(self):
        min = 1
        max = 5
        interval = 0.5

        asserted_tpl = split_by_interval(min, max,interval)

        self.assertTrue(asserted_tpl[1]["From"].min() == min)
        self.assertTrue(asserted_tpl[1]["Till"].max() == max)

    def test_check_group(self):
        min = 1
        max = 5
        interval = 0.5

        asserted_tpl = split_by_interval(min, max,interval)

        fr = min
        for index, row in asserted_tpl[1].iterrows():
            self.assertEqual(fr, row["From"])
            self.assertTrue(row["Till"]>row["From"])
            fr = row["Till"]
        self.assertEqual(max,fr)

class ClassifyPriceSrByGroupTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_group_index(self):
        min = 0
        max = 10
        count = 5
        interval, groups = split_by_count(min,max, count)

        price_sr = pd.Series([0, 4, 6, 9])
        
        expected_groups_sr = pd.Series([1,2,3,5])

        asserted_groups_sr = classify_price_sr_by_group(price_sr,groups[group_col_name])
        
        self.assertTrue(asserted_groups_sr.equals(expected_groups_sr))
