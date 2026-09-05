import unittest

import pandas as pd

from src.stockpilot.baseline import (
    create_seasonal_naive_forecast,
    calculate_forecast_metrics)


class TestSeasonalNaiveForecast(unittest.TestCase):
    def test_forecast_repeats_last_training_week(self):
        train_sales = pd.DataFrame(
            {
                "date": pd.to_datetime(
                    [
                        "2017-09-24",
                        "2017-09-25",
                        "2017-09-26",
                        "2017-09-27",
                        "2017-09-28",
                        "2017-09-29",
                        "2017-09-30",
                    ]
                ),
                "store": [1, 1, 1, 1, 1, 1, 1],
                "item": [1, 1, 1, 1, 1, 1, 1],
                "sales": [10, 20, 30, 40, 50, 60, 70],
            }
        )

        test_sales = pd.DataFrame(
            {
                "date": pd.to_datetime(
                    ["2017-10-01", "2017-10-02", "2017-10-08"]
                ),
                "store": [1, 1, 1],
                "item": [1, 1, 1],
                "sales": [12, 22, 14],
            }
        )

        forecast = create_seasonal_naive_forecast(
            train_sales,
            test_sales,
        )

        self.assertEqual(
            forecast["prediction"].tolist(),
            [10, 20, 10],
        )


    def test_forecast_does_not_modify_test_data(self):
        train_sales = pd.DataFrame(
            {
                "date": pd.to_datetime(["2017-09-24"]),
                "store": [1],
                "item": [1],
                "sales": [10],
            }
        )

        test_sales = pd.DataFrame(
            {
                "date": pd.to_datetime(["2017-10-01"]),
                "store": [1],
                "item": [1],
                "sales": [12],
            }
        )

        original_test_sales = test_sales.copy()

        create_seasonal_naive_forecast(
            train_sales,
            test_sales,
        )

        pd.testing.assert_frame_equal(
            test_sales,
            original_test_sales,
        )


class TestForecastMetrics(unittest.TestCase):
    def test_calculates_mae_and_rmse(self):
        forecast = pd.DataFrame(
            {
                "sales":[12,22,14],
                "prediction": [10,20,10],
            }
        )

        metrics = calculate_forecast_metrics(forecast)

        self.assertAlmostEqual(
            metrics["mae"],
            8/3,
        )
        self.assertAlmostEqual(
            metrics["rmse"],
            8**0.5,
        )
