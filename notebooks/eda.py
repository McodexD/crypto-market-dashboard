import pandas as pd
import duckdb

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 10)


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)



section("PANDAS — Loading and basic structure")
markets = pd.read_csv("data/markets.csv")
history = pd.read_csv("data/history.csv", parse_dates=["date"])

print("markets.csv shape:", markets.shape)
print("history.csv shape:", history.shape)
print("\nmarkets.csv dtypes:\n", markets.dtypes)
print("\nmarkets.csv head:\n", markets.head())

section("PANDAS — Missing values check")
print(markets.isna().sum())

section("PANDAS — Summary statistics")
print(markets[["price_usd", "market_cap_usd", "volume_24h_usd", "price_change_pct_24h"]].describe())

section("PANDAS — Top 10 coins by market cap")
top10 = markets.sort_values("market_cap_usd", ascending=False).head(10)
print(top10[["name", "price_usd", "market_cap_usd", "price_change_pct_24h"]])

section("PANDAS — Biggest 24h gainers and losers")
gainers = markets.sort_values("price_change_pct_24h", ascending=False).head(5)
losers = markets.sort_values("price_change_pct_24h", ascending=True).head(5)
print("Top gainers:\n", gainers[["name", "price_change_pct_24h"]])
print("\nTop losers:\n", losers[["name", "price_change_pct_24h"]])

section("PANDAS — Price history: date range and coins covered")
print("Date range:", history["date"].min(), "to", history["date"].max())
print("Coins in history:", history["coin_id"].unique())

section("PANDAS — Average price per coin over the full period")
print(history.groupby("coin_id")["price_usd"].agg(["mean", "min", "max"]))




section("DUCKDB — Same top-10-by-market-cap, as SQL")
result = duckdb.sql("""
    SELECT name, price_usd, market_cap_usd, price_change_pct_24h
    FROM 'data/markets.csv'
    ORDER BY market_cap_usd DESC
    LIMIT 10
""").df()
print(result)

section("DUCKDB — Market cap distribution by rough price bracket")
result = duckdb.sql("""
    SELECT
        CASE
            WHEN price_usd < 1 THEN 'under $1'
            WHEN price_usd < 100 THEN '$1 - $100'
            WHEN price_usd < 10000 THEN '$100 - $10,000'
            ELSE 'over $10,000'
        END AS price_bracket,
        COUNT(*) AS num_coins,
        SUM(market_cap_usd) AS total_market_cap
    FROM 'data/markets.csv'
    GROUP BY price_bracket
    ORDER BY total_market_cap DESC
""").df()
print(result)

section("DUCKDB — 7-day rolling average price per coin (window function)")
result = duckdb.sql("""
    SELECT
        coin_id,
        date,
        price_usd,
        AVG(price_usd) OVER (
            PARTITION BY coin_id
            ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS rolling_7day_avg
    FROM 'data/history.csv'
    ORDER BY coin_id, date
""").df()
print(result.head(15))

section("DUCKDB — Overall price volatility per coin (stddev)")
result = duckdb.sql("""
    SELECT
        coin_id,
        ROUND(AVG(price_usd), 2) AS avg_price,
        ROUND(STDDEV(price_usd), 2) AS price_stddev
    FROM 'data/history.csv'
    GROUP BY coin_id
    ORDER BY price_stddev DESC
""").df()
print(result)

print("\nEDA complete.")
