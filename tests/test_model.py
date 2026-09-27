import unittest

import pandas as pd

from src.stockpilot.model import train_demand_model, predict_demand


class TestDemandModel(unittest.TestCase):
    def test_predicts_without_future_sales(self):
        development_sales = pd.DataFrame(
            {
                "date": pd.date_range(
                    start="2013-01-01",
                    periods=28,
                    freq="D",
                ),
                "store": [1] * 28,
                "item": [1] * 28,
                "sales": [10] * 28,
            }
        )

        future_sales = pd.DataFrame(
            {
                "date": pd.to_datetime(
                    ["2013-01-29", "2013-01-30"]
                ),
                "store": [1, 1],
                "item": [1, 1],
            },
            index=[100, 101],
        )
        original_future_sales = future_sales.copy()

        model = train_demand_model(development_sales)
        forecast = predict_demand(model, future_sales)

        self.assertEqual(len(forecast), 2)
        self.assertEqual(forecast.index.tolist(), [100, 101])
        self.assertIn("prediction", forecast.columns)

        for prediction in forecast["prediction"]:
            self.assertAlmostEqual(prediction, 10.0)

        pd.testing.assert_frame_equal(
            future_sales,
            original_future_sales,
        )