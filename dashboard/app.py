import pandas as pd
import streamlit as st

st.set_page_config(page_title="Crypto Market Dashboard", layout="wide")


@st.cache_data
def load_markets():
    return pd.read_csv("data/markets.csv")


@st.cache_data
def load_history():
    return pd.read_csv("data/history.csv", parse_dates=["date"])


def render_kpis(df):
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Market Cap", f"${df['market_cap_usd'].sum() / 1e12:.2f}T")
    col2.metric("Coins Tracked", len(df))
    col3.metric("Avg 24h Change", f"{df['price_change_pct_24h'].mean():.2f}%")


def render_filters(df):
    names = sorted(df["name"].unique())
    selected = st.sidebar.multiselect("Filter by coin", names, default=names[:10])
    return selected


def render_bar_chart(df, selected):
    filtered = df[df["name"].isin(selected)] if selected else df
    top = filtered.sort_values("market_cap_usd", ascending=False).set_index("name")
    st.subheader("Market Cap by Coin")
    st.bar_chart(top["market_cap_usd"])


def render_line_chart(history, markets, selected):
    if selected:
        ids = markets[markets["name"].isin(selected)]["id"].tolist()
        history = history[history["coin_id"].isin(ids)]
    pivot = history.pivot_table(index="date", columns="coin_id", values="price_usd", aggfunc="mean")
    st.subheader("Price History")
    st.line_chart(pivot)


def main():
    st.title("Crypto Market Dashboard")

    markets = load_markets()
    history = load_history()

    render_kpis(markets)
    selected = render_filters(markets)
    render_bar_chart(markets, selected)
    render_line_chart(history, markets, selected)


if __name__ == "__main__":
    main()