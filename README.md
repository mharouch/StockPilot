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

Only `train.csv` is required for the first version of the project.

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

## Repository Structure

- `data/raw/`: original dataset files stored locally
- `data/processed/`: cleaned or transformed datasets
- `notebooks/`: exploratory analysis notebooks
- `src/stockpilot/`: reusable Python modules
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

## Data Policy

Original dataset files remain unchanged inside `data/raw/`.

Processed or generated data will be stored separately inside `data/processed/`.

Any simulated business data will be explicitly identified to avoid confusion with the original Kaggle dataset.
