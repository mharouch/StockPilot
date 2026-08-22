import unittest

import pandas as pd

from src.stockpilot.data_split import split_sales_data


class TestSplitSalesData(unittest.TestCase):
    def test_split_sales_before_and_after_start_date(self):
        sales = pd.DataFrame(
            {
                "date": pd.to_datetime(
                    ["2017-09-30", "2017-10-01", "2017-10-02"]
                ),
                "store": [1, 1, 1],
                "item": [1, 1, 1],
                "sales": [10, 20, 30],
            }
        )

        train_sales, test_sales = split_sales_data(sales)

        self.assertEqual(len(train_sales), 1)
        self.assertEqual(len(test_sales), 2)
        self.assertLess(
            train_sales["date"].max(),
            test_sales["date"].min(),
        )

    def test_split_rejects_empty_test_dataset(self):
        sales = pd.DataFrame(
            {
                "date": pd.to_datetime(["2017-09-29", "2017-09-30"]),
                "store": [1, 1],
                "item": [1, 1],
                "sales": [10, 20],
            }
        )

        with self.assertRaises(ValueError):
            split_sales_data(sales)
