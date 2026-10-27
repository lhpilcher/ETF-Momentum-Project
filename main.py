import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op

# ETFs to analyze
tickers = ["VOO", "QQQ", "IWM", "VXUS", "TLT", "GLD"]

# Download historical adjusted prices
data = yf.download(
    tickers,
    start="2015-01-01",
    end="2026-01-01",
    auto_adjust=True,
    progress=False
)

# Extract closing prices
prices = data["Close"].dropna()
print(prices)

def calculate_momentum(prices, lookback=63):
    current_prices = prices.iloc[-1]
    past_prices = prices.iloc[-(lookback+1)]
    momentum = ((current_prices / past_prices) - 1)
    return momentum

momentum = calculate_momentum(prices)

ranked_momentum = momentum.sort_values(ascending=False)

print(ranked_momentum)

returns = prices.pct_change()
momentum = prices.pct_change(63)  # momentum for every date
 
# Last trading day of each month
rebalance_dates = prices.groupby(prices.index.to_period("M")).tail(1).index
 
weights = pd.DataFrame(np.nan, index=prices.index, columns=prices.columns)
 
for date in rebalance_dates:
    mom = momentum.loc[date].dropna()
    if mom.empty:
        continue
    top = mom.nlargest(3).index
    weights.loc[date] = 0.0
    weights.loc[date, top] = 1 / 3
 
weights = weights.ffill().fillna(0)
 
# Shift by 1 day: signal at close of day t is traded on day t+1 (no look-ahead)
strat_ret = (weights.shift(1) * returns).sum(axis=1)
 
# Transaction costs: 5 bps per unit of turnover
turnover = weights.diff().abs().sum(axis=1)
strat_ret = strat_ret - turnover * 0.0005
 
# Benchmarks
voo_ret = returns["VOO"]
ew_ret = returns.mean(axis=1)  # equal-weight all six (daily rebalanced)
 
# Start everything on the first date a signal could trade
start = weights[weights.sum(axis=1) > 0].index[0]
curves = pd.DataFrame({
    "Momentum": strat_ret,
    "VOO": voo_ret,
    "EqualWeight": ew_ret,
}).loc[start:].dropna()
 
 
# ---------------------------------------------------------------
# 4. Metrics
# ---------------------------------------------------------------
def metrics(r):
    r = r.dropna()
    cum = (1 + r).cumprod()
    years = len(r) / 252
    cagr = cum.iloc[-1] ** (1 / years) - 1
    vol = r.std() * np.sqrt(252)
    sharpe = r.mean() / r.std() * np.sqrt(252)  # risk-free rate assumed 0
    max_dd = (cum / cum.cummax() - 1).min()
    return pd.Series({"CAGR": cagr, "Vol": vol, "Sharpe": sharpe, "MaxDD": max_dd})
 
 
results = pd.DataFrame({name: metrics(curves[name]) for name in curves}).T
print("\nPerformance summary:")
print(results.round(3))
 
 
# ---------------------------------------------------------------
# 5. Plots
# ---------------------------------------------------------------
growth = (1 + curves).cumprod()
drawdown = growth / growth.cummax() - 1
 
fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
growth.plot(ax=axes[0], title="Growth of $1")
drawdown.plot(ax=axes[1], title="Drawdown")
plt.tight_layout()
plt.show()

