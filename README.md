# StockPilot

StockPilot analyzes historical retail sales and forecasts daily demand by store and item.

Alpha 1 is a standalone demand forecasting engine. Inventory management is planned for future versions.

## Project Objectives

Alpha 1 provides the following capabilities:

- validate and prepare historical sales data
- explore sales by store, item, and period
- identify trends and seasonal patterns
- forecast future demand

Stock management, replenishment recommendations, and a user interface are possible future extensions.

## Dataset

The project uses the Kaggle dataset **Store Item Demand Forecasting Challenge**.

Dataset page: https://www.kaggle.com/competitions/demand-forecasting-kernels-only/data

The dataset contains approximately five years of daily sales data for:

- 10 stores
- 50 items
- approximately 913,000 sales records

The main columns available in the training dataset are:

- `date`: date of the sales record
- `store`: store identifier
- `item`: item identifier
- `sales`: number of units sold

The dataset is treated as a realistic retail sales dataset. It is not presented as certified data from a specific real-world company.

## Dataset Limitations

The original dataset does not contain some information commonly required for inventory management, including:

- historical inventory levels
- product prices
- promotions
- supplier orders
- delivery lead times
- storage costs
- stockout history
- product names and categories

When required in later versions, these business variables will be simulated and clearly separated from the original sales data.

## Dataset Setup

Raw data files must be downloaded manually from Kaggle and placed in the following local directory:

`data/raw/`

Expected files:

- `train.csv`
- `test.csv`
- `sample_submission.csv`

Only `train.csv` is required for the current analysis and forecasting commands. Validation and final test periods are held out from this file; Kaggle's `test.csv` is not used.

The raw dataset files are not committed to the Git repository. The `data/raw/` directory is reserved for local, unmodified source data.

## Alpha 1: Data Analysis and Forecasting

Alpha 1 covers data validation, exploratory analysis, a seasonal naive baseline, model selection, and final demand forecast evaluation.

### Data analysis

The dataset is checked for structure, date range, missing values, and duplicates. The exploratory notebook examines sales by store, item, and time period, including seasonal patterns.

The analysis produced the following findings:

- the dataset contains 913,000 daily sales records covering 10 stores and 50 items from 2013 to 2017
- no missing values or duplicated rows were identified
- Store 2 records the highest total sales, while Store 7 records the lowest
- Items 15 and 28 record the highest total sales
- daily sales show an overall upward trend across the five-year period
- average sales follow a strong weekly pattern, with the lowest level on Monday and the highest on Sunday
- average sales follow a strong annual pattern, generally increasing from January to July before declining during the second half of the year

These findings describe the observed sales patterns but do not explain their business causes. The missing inventory, pricing, promotion, product, and store information limits the conclusions that can be drawn from the dataset.

### Forecasting

The seasonal naive baseline repeats the last training week's sales by store, item, and weekday. A single `HistGradientBoostingRegressor` predicts daily sales across all stores and items using store, item, weekday, month, day of year, and days since 2013-01-01. Actual sales are the training target, not an input feature.

#### Model selection

Models were trained on 2013-01-01–2017-06-30 (821,000 rows) and compared on 2017-07-01–2017-09-30 (46,000 rows). Parameters were selected by validation MAE.

| Model | `max_iter` | `max_leaf_nodes` | MAE | RMSE |
|---|---:|---:|---:|---:|
| Seasonal naive | — | — | 10.48 | 13.66 |
| Gradient boosting | 100 | 31 | 6.64 | 8.66 |
| Gradient boosting | 200 | 31 | 6.66 | 8.69 |
| Gradient boosting (selected) | 200 | 15 | 6.57 | 8.57 |

All boosting runs use `learning_rate=0.1`, `early_stopping=False`, and `random_state=42`. Store, item, weekday, and month are treated as categorical features.

#### Final evaluation

The selected model was retrained on 2013-01-01–2017-09-30 (867,000 rows) and evaluated on 2017-10-01–2017-12-31 (46,000 rows). This test period was not used to select its parameters.

| Model | MAE | RMSE |
|---|---:|---:|
| Seasonal naive | 12.02 | 15.92 |
| Gradient boosting (200 iterations, 15 leaves maximum) | 5.87 | 7.59 |

Compared with the baseline on the same test rows, MAE fell by 51.2% and RMSE by 52.3% (rounded scores). MAE is the mean absolute error in units sold per store-item-day; RMSE penalizes larger errors more heavily. Lower is better for both.

These results cover one test quarter. They do not establish performance in other periods or measure reductions in stockouts or inventory costs.

The tables record the original evaluation. A rerun with scikit-learn 1.9.1 and NumPy 2.4.6 produced MAE 5.84 and RMSE 7.55 for the selected model on the final test period. Dependency versions are not pinned, so small differences may occur.

## Repository Structure

- `data/raw/`: original dataset files stored locally
- `data/processed/`: cleaned or transformed datasets
- `notebooks/`: exploratory analysis notebooks
- `src/stockpilot/`: reusable Python modules
- `tests/`: automated tests
- `requirements.txt`: Python dependencies
- `README.md`: project documentation

## Installation

### Prerequisites

- Python 3.11 or later
- Git
- A Kaggle account to download the dataset

### Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/mharouch/StockPilot.git
cd StockPilot
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the required Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Download the dataset as described in the **Dataset Setup** section before running the analysis.

## Usage

Run the dataset validation script from the project root:

```bash
python src/stockpilot/data_validation.py
```

The script displays:

- the first five rows
- the dataset dimensions
- the column names and data types
- the covered date range
- missing-value counts
- duplicated-row counts

The exploratory analysis is available in:

`notebooks/01_initial_sales_exploration.ipynb`

Open the notebook in a Jupyter-compatible editor, select the `.venv` Python environment, and run all cells in order.

Compare the three model configurations on validation data:

```bash
python -m src.stockpilot.model
```

Retrain the selected configuration and compare it with the baseline on the final test period:

```bash
python -m src.stockpilot.evaluate_model
```

Both commands run from the project root and print MAE and RMSE. Models are trained in memory and are not saved.

To also save the final test predictions, run:

```bash
python -m src.stockpilot.evaluate_model --export-csv
```

The command writes `data/processed/forecasts.csv` with columns `date`, `store`, `item`, `actual_sales`, and `predicted_sales`. The rows cover the historical test period (October–December 2017).

Run automated tests:

```bash
python -m unittest discover -s tests -v
```

## Data Policy

Original dataset files remain unchanged inside `data/raw/`.

Processed or generated data will be stored separately inside `data/processed/`.

Any simulated business data will be explicitly identified to avoid confusion with the original Kaggle dataset.
