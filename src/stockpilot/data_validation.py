import pandas as pd


DATA_PATH = "data/raw/train.csv"


def load_sales_data(file_path):
    """Load sales data from a CSV file."""
    return pd.read_csv(file_path, parse_dates=["date"])


def main():
    sales = load_sales_data(DATA_PATH)
    print(sales.head())


if __name__ == "__main__":
    main()