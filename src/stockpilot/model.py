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


def create_demand_model():
    """Create the histogram gradient boosting demand model."""
    return HistGradientBoostingRegressor(
        categorical_features=CATEGORICAL_FEATURES,
        learning_rate=0.1,
        max_iter=100,
        max_leaf_nodes=31,
        early_stopping=False,
        random_state=RANDOM_STATE,
    )


def train_demand_model(development_sales):
    """Train the demand model using development sales only."""
    features = create_calendar_features(development_sales)
    target = development_sales["sales"]

    model = create_demand_model()
    model.fit(features, target)

    return model


def predict_demand(model, sales):
    """Generate demand predictions for the supplied sales rows."""
    features = create_calendar_features(sales)

    forecast = sales.copy()
    forecast["prediction"] = model.predict(features)

    return forecast

def main():
    """Compare the demand model and baseline on validation data."""
    sales = load_sales_data(DATA_PATH)
    development_sales, validation_sales, _ = (
        split_sales_for_model_selection(sales)
    )

    print("Training the demand model...")
    model = train_demand_model(development_sales)

    model_forecast = predict_demand(model, validation_sales)
    model_metrics = calculate_forecast_metrics(model_forecast)

    baseline_forecast = create_seasonal_naive_forecast(
        development_sales,
        validation_sales,
    )
    baseline_metrics = calculate_forecast_metrics(baseline_forecast)

    print(f"Validation predictions: {len(model_forecast)}")

    print("\nSeasonal naive baseline:")
    print(f"MAE: {baseline_metrics['mae']:.2f}")
    print(f"RMSE: {baseline_metrics['rmse']:.2f}")

    print("\nHistGradientBoostingRegressor:")
    print(f"MAE: {model_metrics['mae']:.2f}")
    print(f"RMSE: {model_metrics['rmse']:.2f}")


if __name__ == "__main__":
    main()