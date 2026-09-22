# IPL Data Pipeline & Power BI Dashboard

An automated ETL pipeline that cleans IPL match and ball-by-ball data (2008-2024),
loads it into a SQL database, and powers an interactive Power BI dashboard.
Includes a hypothesis test to check whether winning the toss gives a real advantage.

## Tech Stack
Python, Pandas, SQLAlchemy, SQLite, Statsmodels, Power BI

## What it does
- Extracts raw IPL data from CSV files
- Cleans it: fixes inconsistent team names (e.g. Delhi Daredevils -> Delhi Capitals), handles missing values, fixes data types
- Loads clean data into a SQLite database and processed CSVs
- Runs a statistical hypothesis test on toss advantage
- Feeds a Power BI dashboard with KPIs, team/player comparisons, and slicers

## Key Finding
Using a proportion z-test, winning the toss does **not** give a statistically significant advantage in IPL matches (p = 0.586, toss winner won 50.8% of matches).

## How to run

1. Download `matches.csv` and `deliveries.csv` from Kaggle (search "IPL dataset") and place them in `data/raw/`

2. Create a virtual environment and install dependencies:

python -m venv venv
venv\Scripts\activate
pip install pandas sqlalchemy statsmodels


3. Run the pipeline:

python run_pipeline.py


4. Run the hypothesis test:

python hypothesis_test.py


5. Open `IPL.pbix` in Power BI Desktop to view the dashboard

## Dashboard
*(Add a screenshot of your Power BI dashboard here once you export one)*

## Data Source
[Kaggle IPL Dataset](https://www.kaggle.com/) (search "IPL dataset matches deliveries")