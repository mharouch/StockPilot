import argparse
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from src.stockpilot.baseline import (
    calculate_forecast_metrics,
    create_seasonal_naive_forecast,
)
from src.stockpilot.data_split import split_sales_data
from src.stockpilot.data_validation import DATA_PATH, load_sales_data
from src.stockpilot.model import predict_demand, train_demand_model


SELECTED_MAX_ITER = 200
SELECTED_MAX_LEAF_NODES = 15
FORECAST_CSV_PATH = Path("data/processed/forecasts.csv")


def export_forecasts_to_csv(forecast, destination):
    """Write the historical test predictions to a CSV file."""
    keys = ["date", "store", "item"]
    results = forecast.loc[:, keys + ["sales", "prediction"]].rename(
        columns={"sales": "actual_sales", "prediction": "predicted_sales"}
    )
    results["date"] = pd.to_datetime(results["date"]).dt.normalize()
    numeric_columns = ["store", "item", "actual_sales", "predicted_sales"]
    results[numeric_columns] = results[numeric_columns].apply(pd.to_numeric)

    if results["date"].isna().any() or not np.isfinite(
        results[numeric_columns].to_numpy(dtype=float, na_value=np.nan)
    ).all():
        raise ValueError("Forecast rows must have a date and finite numeric values.")
    if results.duplicated(keys).any():
        raise ValueError("Forecast rows must be unique by date, store, and item.")

    results = results.sort_values(keys)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=destination.parent) as directory:
        temporary_path = Path(directory) / destination.name
        results.to_csv(temporary_path, index=False, date_format="%Y-%m-%d")
        temporary_path.replace(destination)


def main(export_csv=False):
    """Evaluate the selected model on the final test period."""
    sales = load_sales_data(DATA_PATH)
    train_sales, test_sales = split_sales_data(sales)

    print(f"Training rows: {len(train_sales)}")
    print(f"Test rows: {len(test_sales)}")
    print("Training the selected model...")

    model = train_demand_model(
        train_sales,
        max_iter=SELECTED_MAX_ITER,
        max_leaf_nodes=SELECTED_MAX_LEAF_NODES,
    )

    forecast = predict_demand(model, test_sales)
    metrics = calculate_forecast_metrics(forecast)

    baseline_forecast = create_seasonal_naive_forecast(
        train_sales,
        test_sales,
    )
    baseline_metrics = calculate_forecast_metrics(baseline_forecast)

    print("\nFinal test: October–December 2017")

    print("\nSeasonal naive baseline:")
    print(f"MAE: {baseline_metrics['mae']:.2f}")
    print(f"RMSE: {baseline_metrics['rmse']:.2f}")

    print("\nSelected gradient boosting model:")
    print(f"MAE: {metrics['mae']:.2f}")
    print(f"RMSE: {metrics['rmse']:.2f}")

    if export_csv:
        export_forecasts_to_csv(forecast, FORECAST_CSV_PATH)
        print(f"\nForecasts saved to {FORECAST_CSV_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        "--export-csv",
        action="store_true",
        help=f"Save the final test predictions to {FORECAST_CSV_PATH}.",
    )
    main(export_csv=parser.parse_args().export_csv)
