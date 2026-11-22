import csv
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd

from src.stockpilot.evaluate_model import export_forecasts_to_csv


class TestExportForecastsToCsv(unittest.TestCase):
    def setUp(self):
        self.forecast = pd.DataFrame(
            {
                "date": pd.to_datetime(["2017-10-02", "2017-10-01", "2017-10-01"]),
                "store": [1, 2, 1],
                "item": [2, 1, 1],
                "sales": [12, 9, 6],
                "prediction": [11.5, 8.75, 6.25],
            },
            index=[42, 17, 23],
        )

    def test_exports_sorted_rows_without_mutating_forecast(self):
        original = self.forecast.copy()

        with TemporaryDirectory() as directory:
            destination = Path(directory) / "processed" / "forecasts.csv"
            export_forecasts_to_csv(self.forecast, destination)
            with destination.open(newline="") as file:
                rows = list(csv.reader(file))

        self.assertEqual(
            rows,
            [
                ["date", "store", "item", "actual_sales", "predicted_sales"],
                ["2017-10-01", "1", "1", "6", "6.25"],
                ["2017-10-01", "2", "1", "9", "8.75"],
                ["2017-10-02", "1", "2", "12", "11.5"],
            ],
        )
        pd.testing.assert_frame_equal(self.forecast, original)

    def test_reexport_replaces_previous_rows(self):
        with TemporaryDirectory() as directory:
            destination = Path(directory) / "forecasts.csv"
            export_forecasts_to_csv(self.forecast, destination)
            export_forecasts_to_csv(self.forecast.iloc[:1], destination)
            result = pd.read_csv(destination)

        self.assertEqual(result["date"].tolist(), ["2017-10-02"])
        self.assertEqual(result["predicted_sales"].tolist(), [11.5])

    def test_rejects_missing_values_and_nonfinite_predictions(self):
        for column, value in [("date", pd.NaT), ("prediction", float("inf"))]:
            with self.subTest(column=column), TemporaryDirectory() as directory:
                invalid = self.forecast.copy()
                invalid.loc[42, column] = value
                destination = Path(directory) / "forecasts.csv"
                with self.assertRaisesRegex(ValueError, "date and finite numeric"):
                    export_forecasts_to_csv(invalid, destination)
                self.assertFalse(destination.exists())

    def test_rejects_duplicate_date_store_item_keys(self):
        duplicate = pd.concat([self.forecast, self.forecast.iloc[:1]])
        with TemporaryDirectory() as directory:
            destination = Path(directory) / "forecasts.csv"
            with self.assertRaisesRegex(ValueError, "unique by date, store, and item"):
                export_forecasts_to_csv(duplicate, destination)
            self.assertFalse(destination.exists())
