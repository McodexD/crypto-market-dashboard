# Crypto Market Dashboard

A data visualization project combining data engineering and UX design principles, built around live cryptocurrency market data. Solo DE build for the STI Datavisualisering course, targeting VG.

**Live app:** [crypto-market-dashboard.streamlit.app](https://crypto-market-dashboard-t785dcsqqgh7vfaaxxyqgp.streamlit.app)

---

## Overview

This project pulls live cryptocurrency market data from the CoinGecko API and turns it into a full pipeline of exploration, visualization, and storytelling:

- Data collection from a public API
- Exploratory data analysis in pandas and duckdb
- An interactive Power BI dashboard, published to the Power BI Service
- Two matplotlib charts built around a clear narrative, not just raw plots
- A deployed, interactive Streamlit dashboard

## Tech Stack

| Layer | Tools |
|---|---|
| Data source | [CoinGecko API](https://www.coingecko.com/en/api) (free, no key required) |
| Data handling | pandas, duckdb |
| Visualization | matplotlib, Power BI Desktop |
| App | Streamlit, deployed on Streamlit Community Cloud |
| Workflow | GitHub (branches, issues, pull requests) |

## Project Structure

```
crypto-market-dashboard/
├── data/
│   ├── markets.csv          # snapshot of 50 coins: price, market cap, volume, 24h change
│   └── history.csv          # 90-day hourly price history for 5 major coins
├── notebooks/
│   └── eda.py                # EDA in pandas and duckdb
├── charts/
│   ├── 01_market_cap_concentration.png
│   ├── 02_24h_sentiment.png
│   └── storytelling.py       # generates the two charts above
├── powerbi/
│   └── dashboard.pbix        # KPIs, filters, bar chart, line chart
├── dashboard/
│   └── app.py                 # Streamlit app: KPIs, filters, bar chart, line chart
├── fetch_data.py               # pulls live data from CoinGecko into data/
└── requirements.txt
```

## Features

**EDA** — structure checks, summary statistics, top gainers/losers, and duckdb SQL including a rolling average window function and volatility comparison.

**Power BI Dashboard** — 3 KPI cards (total market cap, coins tracked, average 24h change), a coin-name filter, a bar chart of market cap by coin, and a line chart of price history. Published to the Power BI Service.

**Data Storytelling** — two charts, each built around a stated headline insight rather than a generic label:
- *Bitcoin alone holds nearly half the tracked market* — a market cap concentration breakdown
- *A red day across the board* — 24h price change across the top 20 coins by market cap, sorted and color-coded

**Streamlit Dashboard** — same core KPIs, filter, bar chart, and line chart as the Power BI version, live and interactive at the link above.

## Running Locally

```
git clone https://github.com/McodexD/crypto-market-dashboard.git
cd crypto-market-dashboard
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python fetch_data.py
streamlit run dashboard/app.py
```

## Data Source

All data comes from [CoinGecko's public API](https://www.coingecko.com/en/api), a free source with no authentication required.
