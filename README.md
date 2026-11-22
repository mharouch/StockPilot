# StockPilot

StockPilot is a Python project for forecasting daily retail sales by store and item. Alpha 1 trains and evaluates a model on historical sales, then lets you export the test predictions and plot them alongside observed sales. Inventory management is outside the scope of this release.

## Quick start

Install Git and Python 3.11 or later. In a macOS or Linux terminal, clone the repository and set up the environment:

```bash
git clone https://github.com/mharouch/StockPilot.git
cd StockPilot
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Download `train.csv` from the [Kaggle Store Item Demand Forecasting Challenge](https://www.kaggle.com/competitions/demand-forecasting-kernels-only/data) and place it in `data/raw/`. This is the only dataset file you need. StockPilot takes its validation and test periods from that file.

From the repository root, run:

```bash
python -m src.stockpilot.evaluate_model --export-csv
python -m src.stockpilot.plot_forecasts --store 1 --item 1
```

The first command prints MAE and RMSE and saves `data/processed/forecasts.csv` with `date`, `store`, `item`, `actual_sales`, and `predicted_sales`. The rows cover October through December 2017, the historical test period. Run the same command without `--export-csv` to print the scores alone.

Run the plotting command after creating the CSV. Both `--store` and `--item` are required. The example saves `data/processed/plots/store_1_item_1.png`. Git ignores the raw data and generated files.

## Dataset and exploration

Kaggle's training file contains 913,000 daily records from January 2013 through December 2017 for 10 stores and 50 items. Its columns are `date`, `store`, `item`, and `sales` (units sold). Run `python src/stockpilot/data_validation.py` from the repository root to inspect the file's structure, date range, missing values, and duplicate rows.

The [exploration notebook](notebooks/01_initial_sales_exploration.ipynb) shows an upward trend over the five years and recurring weekly and annual patterns. Average sales are lowest on Monday, highest on Sunday, and generally rise toward July before declining later in the year.

Open the notebook in a Jupyter-compatible editor, select the `.venv` kernel, and run all cells in order. Set the kernel's working directory to `notebooks/`. The first cell prints the current directory, and the next cell uses its parent to find `data/raw/train.csv`.

The dataset records units sold without inventory or stockout history. It cannot show how much demand went unmet. It also lacks prices and promotions, which limits what the notebook can say about the causes of sales patterns.

## Model and evaluation

The seasonal naive baseline repeats sales from the last training week for each store, item, and weekday. One `HistGradientBoostingRegressor` covers all stores and items. It uses store, item, weekday, month, day of year, and days since January 1, 2013. The first four are categorical features. Observed sales are the training target.

The three boosting configurations were trained through June 30, 2017 (821,000 rows) and compared on July through September 2017 (46,000 rows). The lowest validation MAE came from `max_iter=200` and `max_leaf_nodes=15`. All runs used `learning_rate=0.1`, `early_stopping=False`, and `random_state=42`. Run `python -m src.stockpilot.model` to repeat the validation comparison.

For the final evaluation, the selected configuration was retrained on all 867,000 rows through September 30 and scored on the 46,000 rows from October through December 2017. That quarter was held out during model selection.

| Model | Validation MAE | Validation RMSE | Final test MAE | Final test RMSE |
|---|---:|---:|---:|---:|
| Seasonal naive | 10.48 | 13.66 | 12.02 | 15.92 |
| Gradient boosting (100 iterations, 31 leaves) | 6.64 | 8.66 | | |
| Gradient boosting (200 iterations, 31 leaves) | 6.66 | 8.69 | | |
| Gradient boosting (200 iterations, 15 leaves) | 6.57 | 8.57 | 5.87 | 7.59 |

MAE is the average absolute error in units sold per store, item, and day. RMSE gives more weight to larger errors. Lower values are better for both. The table records the original runs. A rerun with scikit-learn 1.9.1 and NumPy 2.4.6 gave the selected model a final test MAE of 5.84 and RMSE of 7.55. Dependency versions can affect these scores.

The comparison covers one historical quarter. It leaves performance in other periods, stockout rates, and inventory costs unmeasured.

## Tests

From the repository root, run the tests with the virtual environment active. The tests do not require the Kaggle dataset.

```bash
python -m unittest discover -s tests -v
```
