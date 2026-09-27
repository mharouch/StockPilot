from src.stockpilot.baseline import (
    calculate_forecast_metrics,
    create_seasonal_naive_forecast,
)
from src.stockpilot.data_split import split_sales_data
from src.stockpilot.data_validation import DATA_PATH, load_sales_data
from src.stockpilot.model import predict_demand, train_demand_model


SELECTED_MAX_ITER = 200
SELECTED_MAX_LEAF_NODES = 15


def main():
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


if __name__ == "__main__":
    main()