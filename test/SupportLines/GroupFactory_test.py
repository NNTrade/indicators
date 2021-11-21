import unittest
import pandas as pd
import logging
from src.SupportLines.GroupFactory import split_by_count, split_by_interval

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