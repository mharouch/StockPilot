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


def display_quality_checks(sales):
    """Display the date range and basic data quality checks."""
    start_date = sales["date"].min()
    end_date = sales["date"].max()
    missing_values = sales.isna().sum()
    duplicate_rows = sales.duplicated().sum()

    print("\nDate range:")
    print(f"{start_date.date()} to {end_date.date()}")

    print("\nMissing values:")
    print(missing_values)

    print("\nDuplicate rows:")
    print(duplicate_rows)


def main():
    sales = load_sales_data(DATA_PATH)
    display_basic_information(sales)
    display_quality_checks(sales)


if __name__ == "__main__":
    main()