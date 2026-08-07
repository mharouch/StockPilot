# StockPilot

StockPilot analyzes historical sales data to support demand forecasting and inventory replenishment decisions.

The project focuses on a retail-style scenario where a store or inventory manager needs to understand demand patterns, anticipate future sales, and reduce the risk of stockouts or overstock.

## Dataset

The project uses the Kaggle dataset "Store Item Demand Forecasting Challenge".

This dataset contains daily sales for multiple stores and items. It is treated as a realistic sales dataset for a retail inventory use case, not as certified data from a specific real-world company.

The main available columns are:

- date
- store
- item
- sales

Some information commonly used in inventory management is not available in the original dataset, such as historical stock levels, prices, promotions, supplier lead times, storage costs, and past stockouts.

When needed, these business variables will be simulated and clearly separated from the original sales data.

## Dataset Setup

Raw data files must be downloaded manually from Kaggle and placed in the following local directory:

```text
data/raw/