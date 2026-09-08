import unittest

import pandas as pd

from src.stockpilot.data_split import (
    split_sales_data,
    split_sales_for_model_selection
)


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

    def test_split_sales_for_model_selection_periods(self):
        sales = pd.DataFrame(
            {
                "date": pd.to_datetime(
                    [
                        "2017-06-30",
                        "2017-07-01",
                        "2017-09-30",
                        "2017-10-01",
                        "2017-10-02",
                    ]
                ),
                "store": [1, 1, 1, 1, 1],
                "item": [1, 1, 1, 1, 1],
                "sales": [10, 20, 30, 40, 50],
            }
        )

        development_sales, validation_sales, test_sales = (
            split_sales_for_model_selection(sales)
        )

        self.assertEqual(len(development_sales), 1)
        self.assertEqual(len(validation_sales), 2)
        self.assertEqual(len(test_sales), 2)

        self.assertEqual(
            len(development_sales)
            + len(validation_sales)
            + len(test_sales),
            len(sales),
        )

        self.assertLess(
            development_sales["date"].max(),
            validation_sales["date"].min(),
        )

        self.assertLess(
            validation_sales["date"].max(),
            test_sales["date"].min(),
        )
