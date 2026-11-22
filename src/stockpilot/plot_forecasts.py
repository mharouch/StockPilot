import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd


FORECAST_CSV_PATH = Path("data/processed/forecasts.csv")
PLOTS_DIR = FORECAST_CSV_PATH.parent / "plots"
SALES_COLUMNS = ["actual_sales", "predicted_sales"]
REQUIRED_COLUMNS = ["date", "store", "item", *SALES_COLUMNS]


def load_forecasts(path):
    """Read a forecast export and check its column names."""
    try:
        forecasts = pd.read_csv(path)
    except FileNotFoundError as error:
        raise ValueError(
            f"Forecast CSV not found: {path}. Generate it with "
            "python -m src.stockpilot.evaluate_model --export-csv."
        ) from error
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeError) as error:
        raise ValueError(f"Could not read {path} as a forecast CSV.") from error

    missing = [column for column in REQUIRED_COLUMNS if column not in forecasts]
    if missing:
        raise ValueError(f"Forecast CSV is missing columns: {', '.join(missing)}.")
    return forecasts


def select_forecasts(forecasts, store, item):
    """Return validated daily sales for one store and item, sorted by date."""
    identifiers = forecasts[["store", "item"]].apply(pd.to_numeric, errors="coerce")
    if identifiers.isna().any().any() or (identifiers % 1).ne(0).any().any():
        raise ValueError("Forecast CSV contains invalid store or item identifiers.")

    store_rows = identifiers["store"].eq(store)
    if not store_rows.any():
        raise ValueError(f"Store {store} was not found in the forecast CSV.")

    rows = forecasts.loc[store_rows & identifiers["item"].eq(item)].copy()
    if rows.empty:
        raise ValueError(f"Item {item} was not found for store {store}.")

    rows["date"] = pd.to_datetime(rows["date"], format="%Y-%m-%d", errors="coerce")
    if rows["date"].isna().any():
        raise ValueError("Selected forecasts contain invalid dates (expected YYYY-MM-DD).")
    if rows["date"].duplicated().any():
        raise ValueError("Selected forecasts contain multiple rows for the same date.")

    sales = rows[SALES_COLUMNS].apply(pd.to_numeric, errors="coerce")
    if sales.isna().any().any() or sales.isin([float("inf"), float("-inf")]).any().any():
        raise ValueError("Selected forecasts contain missing or invalid sales values.")
    rows[SALES_COLUMNS] = sales
    return rows.sort_values("date")


def save_forecast_plot(rows, store, item, destination):
    """Save the actual and predicted daily sales as a PNG."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots(figsize=(10, 5), layout="constrained")
    try:
        axis.plot(
            rows["date"], rows["actual_sales"],
            label="Actual sales", color="#2166ac", marker=".", markersize=4,
        )
        axis.plot(
            rows["date"], rows["predicted_sales"],
            label="Predicted sales", color="#b24b14", linestyle="--",
            marker=".", markersize=4,
        )
        axis.set(
            title=f"Actual vs. predicted sales: Store {store}, item {item}",
            xlabel="Date",
            ylabel="Sales (units)",
        )
        padding = pd.Timedelta(hours=12)
        axis.set_xlim(rows["date"].min() - padding, rows["date"].max() + padding)
        locator = mdates.AutoDateLocator(minticks=4, maxticks=7)
        axis.xaxis.set_major_locator(locator)
        axis.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
        axis.grid(axis="y", alpha=0.25)
        axis.legend(frameon=False)
        figure.savefig(destination, format="png", dpi=150)
    finally:
        plt.close(figure)


def main():
    parser = argparse.ArgumentParser(description="Plot actual and predicted daily sales.")
    parser.add_argument("--store", type=int, required=True, help="Store ID")
    parser.add_argument("--item", type=int, required=True, help="Item ID")
    args = parser.parse_args()

    destination = PLOTS_DIR / f"store_{args.store}_item_{args.item}.png"
    try:
        forecasts = load_forecasts(FORECAST_CSV_PATH)
        rows = select_forecasts(forecasts, args.store, args.item)
        save_forecast_plot(rows, args.store, args.item, destination)
    except (ValueError, OSError) as error:
        parser.exit(2, f"Error: {error}\n")

    print(f"Plot saved to {destination} ({len(rows)} days)")


if __name__ == "__main__":
    main()
