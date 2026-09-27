import unittest

import pandas as pd

from src.stockpilot.features import create_calendar_features


class TestCalendarFeatures(unittest.TestCase):
    def test_create_calendar_features(self):
        sales = pd.DataFrame(
            {
                "date": pd.to_datetime(
                    ["2013-01-01", "2013-02-01"]
                ),
                "store": [1, 2],
                "item": [10, 20],
                "sales": [5, 10],
            }
        )
        original_sales = sales.copy()

        features = create_calendar_features(sales)

        self.assertEqual(
            features.columns.tolist(),
            [
                "store",
                "item",
                "day_of_week",
                "month",
                "day_of_year",
                "time_index",
            ],
        )
        self.assertEqual(features["store"].tolist(), [1, 2])
        self.assertEqual(features["item"].tolist(), [10, 20])
        self.assertEqual(features["day_of_week"].tolist(), [1, 4])
        self.assertEqual(features["month"].tolist(), [1, 2])
        self.assertEqual(features["day_of_year"].tolist(), [1, 32])
        self.assertEqual(features["time_index"].tolist(), [0, 31])

        pd.testing.assert_frame_equal(
            sales,
            original_sales,
        )
