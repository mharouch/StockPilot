import pandas as pd

TIME_INDEX_START_DATE = pd.Timestamp("2013-01-01")

CATEGORICAL_FEATURES = [
    "store",
    "item",
    "day_of_week",
    "month",
]

def create_calendar_features(sales):
    """Create calendar and trend features available at prediction time."""
    features = pd.DataFrame(index=sales.index)

    features["store"] = sales["store"]
    features["item"] = sales["item"]
    features["day_of_week"] = sales["date"].dt.dayofweek
    features["month"] = sales["date"].dt.month
    features["day_of_year"] = sales["date"].dt.dayofyear
    features["time_index"] = (
        sales["date"] - TIME_INDEX_START_DATE
    ).dt.days

    return features
