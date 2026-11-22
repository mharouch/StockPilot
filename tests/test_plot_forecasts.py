from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd

from src.stockpilot.plot_forecasts import (
    load_forecasts,
    save_forecast_plot,
    select_forecasts,
)


class TestPlotForecasts(unittest.TestCase):
    def setUp(self):
        self.forecasts = pd.DataFrame(
            {
                "date": ["2017-10-02", "2017-10-01", "2017-10-01", "2017-10-01"],
                "store": [1, 2, 1, 1],
                "item": [1, 1, 2, 1],
                "actual_sales": [10, 25, 30, 5],
                "predicted_sales": [11.5, 24.0, 31.0, 6.5],
            }
        )

    def test_selects_one_store_and_item_in_date_order(self):
        rows = select_forecasts(self.forecasts, store=1, item=1)

        self.assertEqual(
            rows["date"].dt.strftime("%Y-%m-%d").tolist(),
            ["2017-10-01", "2017-10-02"],
        )
        self.assertEqual(rows["actual_sales"].tolist(), [5, 10])
        self.assertEqual(rows["predicted_sales"].tolist(), [6.5, 11.5])

    def test_rejects_missing_store_or_item(self):
        with self.assertRaisesRegex(ValueError, "Store 99 was not found"):
            select_forecasts(self.forecasts, store=99, item=1)
        with self.assertRaisesRegex(ValueError, "Item 2 was not found for store 2"):
            select_forecasts(self.forecasts, store=2, item=2)

    def test_reports_missing_csv_with_export_command(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "forecasts.csv"
            with self.assertRaisesRegex(ValueError, "evaluate_model --export-csv"):
                load_forecasts(path)

    def test_rejects_csv_with_missing_columns(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "forecasts.csv"
            self.forecasts.drop(columns="predicted_sales").to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "missing columns: predicted_sales"):
                load_forecasts(path)

    def test_rejects_invalid_dates_and_sales(self):
        for column, value, message in [
            ("date", "2017-02-30", "invalid dates"),
            ("predicted_sales", float("inf"), "invalid sales values"),
        ]:
            with self.subTest(column=column):
                invalid = self.forecasts.copy()
                invalid.loc[0, column] = value
                with self.assertRaisesRegex(ValueError, message):
                    select_forecasts(invalid, store=1, item=1)

    def test_saves_png_in_new_directory(self):
        rows = select_forecasts(self.forecasts, store=1, item=1)
        with TemporaryDirectory() as directory:
            path = Path(directory) / "plots" / "store_1_item_1.png"
            save_forecast_plot(rows, 1, 1, path)

            image = path.read_bytes()
            self.assertTrue(image.startswith(b"\x89PNG\r\n\x1a\n"))
            self.assertGreater(len(image), 8)
