import math


def calculate_order_quantity(
    forecast_demand,
    current_stock,
    incoming_stock,
    safety_stock,
):
    """Return the order quantity for one store-item pair."""
    if (
        forecast_demand < 0
        or current_stock < 0
        or incoming_stock < 0
        or safety_stock < 0
    ):
        raise ValueError("Demand and stock quantities must be non-negative.")

    required_quantity = (
        forecast_demand
        + safety_stock
        - current_stock
        - incoming_stock
    )

    return math.ceil(max(0, required_quantity))


def create_replenishment_recommendations(forecast, stock):
    """Create replenishment recommendations by store and item."""
    forecast_demand = (
        forecast.groupby(
            ["store", "item"],
            as_index=False,
        )["prediction"]
        .sum()
        .rename(columns={"prediction": "forecast_demand"})
    )

    recommendations = forecast_demand.merge(
        stock,
        on=["store", "item"],
        how="left",
    )

    missing_stock = recommendations[
        [
            "current_stock",
            "incoming_stock",
            "safety_stock",
        ]
    ].isna().any(axis=1)

    if missing_stock.any():
        raise ValueError(
            "Missing stock data for forecasted store-item pairs."
        )

    recommendations["order_quantity"] = recommendations.apply(
        lambda row: calculate_order_quantity(
            forecast_demand=row["forecast_demand"],
            current_stock=row["current_stock"],
            incoming_stock=row["incoming_stock"],
            safety_stock=row["safety_stock"],
        ),
        axis=1,
    )

    return recommendations