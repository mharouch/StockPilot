# StockPilot

StockPilot analyzes historical sales data to support demand forecasting and inventory replenishment decisions.

The project focuses on a retail scenario where a store or inventory manager needs to understand demand patterns, anticipate future sales, and reduce the risk of stockouts and overstock.

## Project Objectives

StockPilot is designed to progressively provide the following capabilities:

- validate and prepare historical sales data
- explore sales by store, item, and period
- identify trends and seasonal patterns
- forecast future demand
- generate inventory replenishment recommendations
- simulate inventory evolution
- measure stockouts, surplus, and inventory costs
- expose results through a dashboard and an API

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

## Version 1: Data Analysis

The first version focuses on understanding the structure, quality, and main characteristics of the sales dataset.

The scope includes:

- load the raw sales dataset
- inspect the available files and columns
- verify the number of rows and columns
- check data types
- identify the covered date range
- check missing values
- check duplicated records
- summarize sales by store, item, and date
- create initial exploratory visualizations
- document the main observations and data-quality issues

Demand forecasting, inventory simulation, the dashboard, the database, and the API are outside the scope of Version 1.

## Version 1 Results

The dataset validation and exploratory analysis produced the following findings:

- the dataset contains 913,000 daily sales records covering 10 stores and 50 items from 2013 to 2017
- no missing values or duplicated rows were identified
- Store 2 records the highest total sales, while Store 7 records the lowest
- Items 15 and 28 record the highest total sales
- daily sales show an overall upward trend across the five-year period
- average sales follow a strong weekly pattern, with the lowest level on Monday and the highest on Sunday
- average sales follow a strong annual pattern, generally increasing from January to July before declining during the second half of the year

These findings describe the observed sales patterns but do not explain their business causes. The missing inventory, pricing, promotion, product, and store information limits the conclusions that can be drawn from the dataset.

## Project Status

Data analysis, demand forecasting, and an initial replenishment rule are implemented. Inventory simulation, the dashboard, the database, and the API are planned.

## Replenishment

Forecast demand is aggregated by store and item. The recommended quantity is calculated as:

`forecast demand + safety stock - current stock - incoming stock`

The forecast input is expected to cover the delivery lead time plus the ordering interval. Current stock represents available inventory, while incoming stock represents expected supplier deliveries. These stock inputs are simulated because they are not included in the original dataset.

Order quantities are rounded up and cannot be negative. Customer backorders and detailed delivery schedules are not yet modeled.

## Forecasting

The seasonal naive baseline repeats the last training week's sales by store, item, and weekday. A single `HistGradientBoostingRegressor` predicts daily sales across all stores and items using store, item, weekday, month, day of year, and days since 2013-01-01. Actual sales are the training target, not an input feature.

### Model selection

Models were trained on 2013-01-01–2017-06-30 (821,000 rows) and compared on 2017-07-01–2017-09-30 (46,000 rows). Parameters were selected by validation MAE.

| Model | `max_iter` | `max_leaf_nodes` | MAE | RMSE |
|---|---:|---:|---:|---:|
| Seasonal naive | — | — | 10.48 | 13.66 |
| Gradient boosting | 100 | 31 | 6.64 | 8.66 |
| Gradient boosting | 200 | 31 | 6.66 | 8.69 |
| Gradient boosting (selected) | 200 | 15 | 6.57 | 8.57 |

All boosting runs use `learning_rate=0.1`, `early_stopping=False`, and `random_state=42`. Store, item, weekday, and month are treated as categorical features.

### Final evaluation

The selected model was retrained on 2013-01-01–2017-09-30 (867,000 rows) and evaluated on 2017-10-01–2017-12-31 (46,000 rows). This test period was not used to select its parameters.

| Model | MAE | RMSE |
|---|---:|---:|
| Seasonal naive | 12.02 | 15.92 |
| Gradient boosting (200 iterations, 15 leaves maximum) | 5.87 | 7.59 |

Compared with the baseline on the same test rows, MAE fell by 51.2% and RMSE by 52.3% (rounded scores). MAE is the mean absolute error in units sold per store-item-day; RMSE penalizes larger errors more heavily. Lower is better for both.

These results cover one test quarter. They do not establish performance in other periods or measure reductions in stockouts or inventory costs.

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

- Python 3.10 or later
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

Run automated tests:

```bash
python -m unittest discover -s tests -v
```

## Data Policy

Original dataset files remain unchanged inside `data/raw/`.

Processed or generated data will be stored separately inside `data/processed/`.

Any simulated business data will be explicitly identified to avoid confusion with the original Kaggle dataset.
