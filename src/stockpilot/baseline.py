import numpy as np
import pandas as pd
from src.stockpilot.data_split import split_sales_data
from src.stockpilot.data_validation import DATA_PATH, load_sales_data


SEASON_LENGTH = 7


def create_seasonal_naive_forecast(train_sales, test_sales):
    """Create a seasonal naive forecast using training data only."""
    train_end_date = train_sales["date"].max()
    reference_start_date = train_end_date - pd.Timedelta(
        days=SEASON_LENGTH - 1
    )

    reference_sales = train_sales[
        (train_sales["date"] >= reference_start_date)
        & (train_sales["date"] <= train_end_date)
    ].copy()

    reference_sales["day_of_week"] = (
        reference_sales["date"].dt.dayofweek
    )

    reference_predictions = reference_sales[
        ["store", "item", "day_of_week", "sales"]
    ].rename(columns={"sales": "prediction"})

    forecast = test_sales.copy()
    forecast["day_of_week"] = forecast["date"].dt.dayofweek

    forecast = forecast.merge(
        reference_predictions,
        on=["store", "item", "day_of_week"],
        how="left",
        validate="many_to_one",
    )

    return forecast.drop(columns="day_of_week")

def calculate_forecast_metrics(forecast):
    """Calculate MAE and RMSE over complete, finite forecast rows."""
    if forecast.empty:
        raise ValueError("Cannot calculate metrics for an empty forecast.")

    values = forecast[["sales", "prediction"]].to_numpy(
        dtype=float, na_value=np.nan
    )
    if not np.isfinite(values).all():
        raise ValueError("Actual sales and predictions must be finite and non-missing.")

    errors = forecast["sales"] - forecast["prediction"]
    mae = errors.abs().mean()
    rmse = errors.pow(2).mean() ** 0.5

    return {"mae": mae, "rmse": rmse}

def main():
    sales = load_sales_data(DATA_PATH)
    train_sales, test_sales = split_sales_data(sales)

    forecast = create_seasonal_naive_forecast(
        train_sales,
        test_sales
    )
    metrics = calculate_forecast_metrics(forecast)

    print("Seasonal naive baseline:")
    print(f"Predictions: {len(forecast)}")
    print(f"MAE: {metrics['mae']:.2f}")
    print(f"RMSE: {metrics['rmse']:.2f}")

if __name__ == "__main__":
    main()
