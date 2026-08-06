# StockPilot

StockPilot is a learning project focused on Python, data analysis, forecasting, inventory management, Git, databases, APIs, and web development.

The goal is to analyze historical sales data, forecast future demand, and progressively build restocking recommendations for a store or inventory manager.

## Dataset

The project will use the Kaggle dataset "Store Item Demand Forecasting Challenge".

This dataset contains daily sales for multiple stores and items. It will be used as a realistic learning dataset, not as certified data from a real retail company.

The main available columns are:

- date
- store
- item
- sales

Some information that would be useful in a real inventory management system is not available in the dataset, such as historical stock levels, prices, promotions, supplier lead times, storage costs, and past stockouts.

These missing business variables may be simulated in later versions of the project. Simulated data will be clearly separated from the original dataset.

## Version 1: Data Analysis

The first version focuses only on understanding and exploring the dataset.

Goals:

- load the dataset
- understand the files and columns
- check missing values
- check duplicates
- identify the time period covered by the data
- explore sales by store, item, and date
- create simple visualizations