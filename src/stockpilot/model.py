from sklearn.ensemble import HistGradientBoostingRegressor

from src.stockpilot.features import (
    CATEGORICAL_FEATURES,
    create_calendar_features,
)
from src.stockpilot.baseline import (
    calculate_forecast_metrics,
    create_seasonal_naive_forecast,
)
from src.stockpilot.data_split import split_sales_for_model_selection
from src.stockpilot.data_validation import DATA_PATH, load_sales_data


RANDOM_STATE = 42


def create_demand_model(max_iter=100, max_leaf_nodes=31):
    """Create the demand model with configurable tree parametrs"""
    return HistGradientBoostingRegressor(
        categorical_features=CATEGORICAL_FEATURES,
        learning_rate=0.1,
        max_iter=max_iter,
        max_leaf_nodes=max_leaf_nodes,
        early_stopping=False,
        random_state=RANDOM_STATE,
    )


def train_demand_model(
    development_sales,
    max_iter=100,
    max_leaf_nodes=31,
):
    """Train the demand model using development sales only."""
    features = create_calendar_features(development_sales)
    target = development_sales["sales"]

    model = create_demand_model(
        max_iter=max_iter,
        max_leaf_nodes=max_leaf_nodes,
    )
    model.fit(features, target)

    return model


def predict_demand(model, sales):
    """Generate demand predictions for the supplied sales rows."""
    features = create_calendar_features(sales)

    forecast = sales.copy()
    forecast["prediction"] = model.predict(features)

    return forecast


def main():
    """Compare model configurations on the validation period."""
    sales = load_sales_data(DATA_PATH)
    development_sales, validation_sales, _ = (
        split_sales_for_model_selection(sales)
    )

    baseline_forecast = create_seasonal_naive_forecast(
        development_sales,
        validation_sales,
    )
    baseline_metrics = calculate_forecast_metrics(baseline_forecast)

    print("Seasonal naive baseline:")
    print(f"MAE: {baseline_metrics['mae']:.2f}")
    print(f"RMSE: {baseline_metrics['rmse']:.2f}")

    configurations = [
        (100, 31),
        (200, 31),
        (200, 15),
    ]

    for max_iter, max_leaf_nodes in configurations:
        print(
            f"\nTraining: max_iter={max_iter}, "
            f"max_leaf_nodes={max_leaf_nodes}"
        )

        model = train_demand_model(
            development_sales,
            max_iter=max_iter,
            max_leaf_nodes=max_leaf_nodes,
        )

        forecast = predict_demand(model, validation_sales)
        metrics = calculate_forecast_metrics(forecast)

        print(f"MAE: {metrics['mae']:.2f}")
        print(f"RMSE: {metrics['rmse']:.2f}")

if __name__ == "__main__":
    main()