import pandas as pd


TEST_START_DATE = "2017-10-01"


def split_sales_data(sales, test_start_date=TEST_START_DATE):
    """Split sales data chronologically into training and test datasets."""
    test_start_date = pd.Timestamp(test_start_date)

    train_sales = sales[sales["date"] < test_start_date].copy()
    test_sales = sales[sales["date"] >= test_start_date].copy()

    return train_sales, test_sales