from datetime import time
import unittest
import pandas as pd
import logging
from src.ElliotWaves.direction import direction

from src.ElliotWaves.waves.impulse_five.search import DataFrameFilter, search_wave


class search_wave_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    def test_filter_by_right_border_for_Long__success(self):
        times = []
        for day in range(6):
            times.append(pd.Timestamp(year=2021, month=1, day=day+1))
        df = pd.DataFrame(data={"H": [3, 5, 7, 10, 8, 5], "L": [
                          2, 4, 6, 8, 1, 4]}, index=times)
        expected_df = pd.DataFrame(
            data={"H": [3, 5, 7, 10], "L": [2, 4, 6, 8]}, index=times[:4])

        srch = DataFrameFilter.getLongFilter()
        asserted_df = srch.filter(df)

        self.assertTrue(asserted_df.index.equals(expected_df.index))
        self.assertTrue(asserted_df["H"].equals(expected_df["H"]))
        self.assertTrue(asserted_df["L"].equals(expected_df["L"]))
        self.assertTrue(asserted_df.equals(expected_df))

    def test_filter_by_right_border_for_Long_by_High__success(self):
        times = []
        for day in range(6):
            times.append(pd.Timestamp(year=2021, month=1, day=day+1))
        df = pd.DataFrame(data={
            "H": [3, 5, 7, 10, 8, 5],
            "L": [2, 4, 6, 8, 6, 4]}, index=times)
        expected_df = pd.DataFrame(
            data={
                "H": [3, 5, 7, 10],
                "L": [2, 4, 6, 8]},
            index=times[:4])

        srch = DataFrameFilter.getLongFilter()
        asserted_df = srch.filter(df)

        self.assertTrue(asserted_df.index.equals(expected_df.index))
        self.assertTrue(asserted_df["H"].equals(expected_df["H"]))
        self.assertTrue(asserted_df["L"].equals(expected_df["L"]))
        self.assertTrue(asserted_df.equals(expected_df))

    def test_filter_by_right_border_for_Long_by_low__success(self):
        times = []
        for day in range(7):
            times.append(pd.Timestamp(year=2021, month=1, day=day+1))
        df = pd.DataFrame(data={
            "H": [3, 5, 7, 10, 10, 12, 14],
            "L": [2, 4, 6, 8, 8, 1, 4]},
            index=times)

        expected_df = pd.DataFrame(data={
            "H": [3, 5, 7, 10, 10],
            "L": [2, 4, 6, 8, 8]},
            index=times[:5])

        srch = DataFrameFilter.getLongFilter()
        asserted_df = srch.filter(df)

        self.assertTrue(asserted_df.index.equals(expected_df.index))
        self.assertTrue(asserted_df["H"].equals(expected_df["H"]))
        self.assertTrue(asserted_df["L"].equals(expected_df["L"]))
        self.assertTrue(asserted_df.equals(expected_df))

    def test_filter_by_right_border_for_Short__success(self):
        times = []
        for day in range(6):
            times.append(pd.Timestamp(year=2021, month=1, day=day+1))
        df = pd.DataFrame(data={"H": [10, 8, 6, 4, 11, 7], "L": [
                          8, 6, 4, 2, 5, 4]}, index=times)
        expected_df = pd.DataFrame(
            data={"H": [10, 8, 6, 4], "L": [8, 6, 4, 2]}, index=times[:4])

        srch = DataFrameFilter.getShortFilter()
        asserted_df = srch.filter(df)

        self.assertTrue(asserted_df.index.equals(expected_df.index))
        self.assertTrue(asserted_df["H"].equals(expected_df["H"]))
        self.assertTrue(asserted_df["L"].equals(expected_df["L"]))
        self.assertTrue(asserted_df.equals(expected_df))

    def test_filter_by_right_border_for_Short_v2__success(self):
        times = []
        for day in range(6):
            times.append(pd.Timestamp(year=2021, month=1, day=day+1))
        df = pd.DataFrame(data={
                "H": [10, 8, 6, 11, 4, 7], 
                "L": [8, 7, 6, 5, 4, 6]}, 
            index=times)
        expected_df = pd.DataFrame(
            data={"H": [10, 8, 6], "L": [8, 7, 6]}, index=times[:3])

        srch = DataFrameFilter.getShortFilter()
        asserted_df = srch.filter(df)

        self.assertTrue(asserted_df.index.equals(expected_df.index))
        self.assertTrue(asserted_df["H"].equals(expected_df["H"]))
        self.assertTrue(asserted_df["L"].equals(expected_df["L"]))
        self.assertTrue(asserted_df.equals(expected_df))

    def test_filter_by_right_border_for_Short_by_Low__success(self):
        times = []
        for day in range(6):
            times.append(pd.Timestamp(year=2021, month=1, day=day+1))
        df = pd.DataFrame(data={"H": [10, 8, 6, 5, 4, 7], "L": [
                          8, 7, 6, 5, 4, 6]}, index=times)
        expected_df = pd.DataFrame(
            data={"H": [10, 8, 6, 5, 4], "L": [8, 7, 6, 5, 4]}, index=times[:5])

        srch = DataFrameFilter.getShortFilter()
        asserted_df = srch.filter(df)

        self.assertTrue(asserted_df.index.equals(expected_df.index))
        self.assertTrue(asserted_df["H"].equals(expected_df["H"]))
        self.assertTrue(asserted_df["L"].equals(expected_df["L"]))
        self.assertTrue(asserted_df.equals(expected_df))

    def test_filter_by_right_border_for_Short_by_High__success(self):
        times = []
        for day in range(6):
            times.append(pd.Timestamp(year=2021, month=1, day=day+1))
        df = pd.DataFrame(data={"H": [10, 8, 6, 11, 4, 7], "L": [
                          8, 7, 6, 5, 4, 3]}, index=times)
        expected_df = pd.DataFrame(
            data={"H": [10, 8, 6], "L": [8, 7, 6]}, index=times[:3])

        srch = DataFrameFilter.getShortFilter()
        asserted_df = srch.filter(df)

        self.assertTrue(asserted_df.index.equals(expected_df.index))
        self.assertTrue(asserted_df["H"].equals(expected_df["H"]))
        self.assertTrue(asserted_df["L"].equals(expected_df["L"]))
        self.assertTrue(asserted_df.equals(expected_df))