import pandas as pd


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
