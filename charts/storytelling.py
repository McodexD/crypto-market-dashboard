import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.edgecolor"] = "#333333"

markets = pd.read_csv("data/markets.csv")

df = markets.sort_values("market_cap_usd", ascending=False).reset_index(drop=True)
top5 = df.head(5).copy()
rest_total = df.iloc[5:]["market_cap_usd"].sum()
total = df["market_cap_usd"].sum()

segments = list(top5["name"]) + ["Other 45 coins"]
values = list(top5["market_cap_usd"]) + [rest_total]
shares = [v / total * 100 for v in values]

colors = ["#F7931A", "#627EEA", "#26A17B", "#F3BA2F", "#23292F", "#D9D9D9"]

fig, ax = plt.subplots(figsize=(10, 3.2))

left = 0
for seg, val, share, color in zip(segments, values, shares, colors):
    ax.barh(0, share, left=left, color=color, edgecolor="white", height=0.6)
    if share > 4:
        ax.text(left + share / 2, 0, f"{seg}\n{share:.0f}%",
                 ha="center", va="center", fontsize=9,
                 color="white" if seg != "Other 45 coins" else "black",
                 fontweight="bold")
    left += share

ax.set_xlim(0, 100)
ax.set_ylim(-1, 1)
ax.axis("off")

top5_share = sum(shares[:5])
fig.suptitle("Bitcoin alone holds nearly half the tracked market",
              fontsize=15, fontweight="bold", x=0.02, ha="left")
ax.set_title(f"Top 5 coins account for {top5_share:.0f}% of total market cap "
             f"across 50 tracked coins", fontsize=10, color="#555555", loc="left", pad=15)

fig.text(0.02, 0.02, "Source: CoinGecko API snapshot, market cap in USD.",
          fontsize=8, color="#888888")

plt.tight_layout(rect=[0, 0.05, 1, 0.92])
plt.savefig("charts/01_market_cap_concentration.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved charts/01_market_cap_concentration.png")

top20 = markets.sort_values("market_cap_usd", ascending=False).head(20).copy()
top20 = top20.sort_values("price_change_pct_24h")

colors2 = ["#D62728" if x < 0 else "#2CA02C" for x in top20["price_change_pct_24h"]]

fig, ax = plt.subplots(figsize=(9, 8))
bars = ax.barh(top20["name"], top20["price_change_pct_24h"], color=colors2)

ax.axvline(0, color="#333333", linewidth=1)

for bar, val in zip(bars, top20["price_change_pct_24h"]):
    x = bar.get_width()
    align = "left" if x < 0 else "right"
    offset = -0.3 if x < 0 else 0.3
    ax.text(x + offset, bar.get_y() + bar.get_height() / 2, f"{val:.1f}%",
             va="center", ha=align, fontsize=8, color="#333333")

ax.spines[["top", "right", "left"]].set_visible(False)
ax.get_xaxis().set_visible(False)
ax.tick_params(axis="y", length=0)

down_count = (top20["price_change_pct_24h"] < 0).sum()
avg_change = top20["price_change_pct_24h"].mean()

fig.suptitle("A red day across the board", fontsize=16, fontweight="bold", x=0.02, ha="left")
ax.set_title(f"{down_count} of the top 20 coins by market cap are down over the last 24h "
             f"(average: {avg_change:.1f}%)", fontsize=10, color="#555555", loc="left", pad=10)

fig.text(0.02, 0.01, "Source: CoinGecko API snapshot, 24h % price change.",
          fontsize=8, color="#888888")

plt.tight_layout(rect=[0, 0.03, 1, 0.94])
plt.savefig("charts/02_24h_sentiment.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved charts/02_24h_sentiment.png")

print("Both storytelling charts complete.")
