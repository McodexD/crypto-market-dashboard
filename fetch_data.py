"""
Pulls two datasets from CoinGecko's free public API (no key required):

1. markets.csv   - a snapshot of the top N coins: price, market cap,
                   24h change, volume. Good for KPIs and bar charts.
2. history.csv   - daily price history for a few selected coins
                   over the last N days. Good for line charts.

Run this from the project root: python fetch_data.py
"""

import requests
import pandas as pd
import time

BASE_URL = "https://api.coingecko.com/api/v3"
TOP_N_COINS = 50
HISTORY_DAYS = 90
HISTORY_COINS = ["bitcoin", "ethereum", "solana", "dogecoin", "cardano"]
SECONDS_BETWEEN_CALLS = 20  # CoinGecko free tier is very strict; slow down hard
MAX_RETRIES = 4


def get_with_retry(url, params):
    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.get(url, params=params)
        if response.status_code == 429:
            wait = 30 * attempt
            print(f"    Rate limited (429). Waiting {wait}s before retry {attempt}/{MAX_RETRIES}...")
            time.sleep(wait)
            continue
        response.raise_for_status()
        return response
    return None  # gave up after retries; caller decides what to do


def fetch_market_snapshot(n=TOP_N_COINS):
    url = f"{BASE_URL}/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": n,
        "page": 1,
        "price_change_percentage": "24h",
    }
    response = get_with_retry(url, params)
    if response is None:
        raise RuntimeError("Could not fetch market snapshot after retries.")
    data = response.json()

    df = pd.DataFrame(data)[
        [
            "id",
            "symbol",
            "name",
            "current_price",
            "market_cap",
            "total_volume",
            "price_change_percentage_24h",
        ]
    ]
    df.columns = [
        "id",
        "symbol",
        "name",
        "price_usd",
        "market_cap_usd",
        "volume_24h_usd",
        "price_change_pct_24h",
    ]
    return df


def fetch_price_history(coin_id, days=HISTORY_DAYS):
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    response = get_with_retry(url, params)
    if response is None:
        print(f"    Giving up on {coin_id} for now, skipping.")
        return None
    data = response.json()

    prices = data["prices"]  # list of [timestamp_ms, price]
    df = pd.DataFrame(prices, columns=["timestamp", "price_usd"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date
    df["coin_id"] = coin_id
    return df[["date", "coin_id", "price_usd"]]


def main():
    print("Fetching market snapshot...")
    markets_df = fetch_market_snapshot()
    markets_df.to_csv("data/markets.csv", index=False)
    print(f"Saved data/markets.csv ({len(markets_df)} coins)")

    print("Fetching price history for selected coins...")
    all_history = []
    skipped = []
    for coin in HISTORY_COINS:
        print(f"  - {coin}")
        history_df = fetch_price_history(coin)
        if history_df is not None:
            all_history.append(history_df)
        else:
            skipped.append(coin)
        time.sleep(SECONDS_BETWEEN_CALLS)

    if all_history:
        combined_history = pd.concat(all_history, ignore_index=True)
        combined_history.to_csv("data/history.csv", index=False)
        print(f"Saved data/history.csv ({len(combined_history)} rows)")

    if skipped:
        print(f"Skipped due to rate limiting: {skipped}")
        print("Run the script again in a minute or two to fill these in "
              "(it will overwrite history.csv, so this only works cleanly "
              "if you fetch all coins in one successful run).")


if __name__ == "__main__":
    main()
