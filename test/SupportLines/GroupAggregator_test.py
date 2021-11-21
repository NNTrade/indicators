import unittest
import pandas as pd
import logging
from src.SupportLines.GroupAggregator import GroupAggregator

class GroupAggregatorTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG)

    def test_group(self):
        df = pd.DataFrame({"g":[101,102,103,104,105,106,107,108,109,110],"v":[10,11,12,13,14,15,16,17,18,19]})

        expected_sr = pd.Series([21,33,36,39,42,45,48,51,54,37])
        
        gragr = GroupAggregator(percent=0.011)
        asserted_sr = gragr.aggregate(df["g"], df["v"])

        self.assertEqual(len(expected_sr), len(asserted_sr))
        for idx in expected_sr.index:
            self.assertEqual(expected_sr[idx], asserted_sr[idx])

