import pandas as pd


TEST_START_DATE = "2017-10-01"


def validate_time_split(sales, train_sales, test_sales):
    """Validate the integrity and chronological order of the split."""
    if train_sales.empty or test_sales.empty:
        raise ValueError("Training and test datasets must not be empty.")

    if len(train_sales) + len(test_sales) != len(sales):
        raise ValueError("Training and test row counts do not match source data.")

    if train_sales["date"].max() >= test_sales["date"].min():
        raise ValueError("Training dates must occur before test dates.")


def split_sales_data(sales, test_start_date=TEST_START_DATE):
    """Split sales data chronologically into training and test datasets."""
    test_start_date = pd.Timestamp(test_start_date)

    train_sales = sales[sales["date"] < test_start_date].copy()
    test_sales = sales[sales["date"] >= test_start_date].copy()

    validate_time_split(sales, train_sales, test_sales)

    return train_sales, test_sales
