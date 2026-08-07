import pandas as pd


DATA_PATH = "data/raw/train.csv"


def load_sales_data(file_path):
    """Load sales data from a CSV file."""
    return pd.read_csv(file_path, parse_dates=["date"])


def display_basic_information(sales):
    """Display the dataset structure and a short preview."""
    print("First five rows:")
    print(sales.head())

    print("\nDataset dimensions:")
    print(f"{sales.shape[0]} rows and {sales.shape[1]} columns")

    print("\nColumns:")
    print(sales.columns.tolist())

    print("\nData types:")
    print(sales.dtypes)


def main():
    sales = load_sales_data(DATA_PATH)
    display_basic_information(sales)


if __name__ == "__main__":
    main()