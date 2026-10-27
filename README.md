Does holding the top 3 momentum ETFs each month beat buy-and-hold VOO, and is the added complexity worth it?

## 🌐 Universe

| Ticker | Exposure |
|--------|----------|
| VOO | US large-cap equities (S&P 500) |
| QQQ | US large-cap growth / Nasdaq-100 |
| IWM | US small-cap equities |
| VXUS | International equities (ex-US) |
| TLT | Long-term US Treasuries |
| GLD | Gold |

**Data:** daily adjusted close prices from Yahoo Finance via `yfinance`, 2015-01-01 to 2026-01-01.

## ⚙️ Strategy

1. Compute 63-day (about 3-month) momentum for every ETF on every date.
2. On the last trading day of each month, rank the ETFs by momentum.
3. Hold the top 3 at equal weight (1/3 each) until the next rebalance.
4. Trade signals on the next day's return (`weights.shift(1)`) to avoid look-ahead bias.
5. Subtract transaction costs of 5 bps per unit of turnover.

## 📊 Benchmarks

- **VOO** buy-and-hold
- **Equal-weight** all six ETFs (daily rebalanced, a simplification)

## 📏 Metrics

CAGR, annualized volatility, Sharpe ratio (risk-free rate assumed 0), and maximum drawdown. The script also plots growth of $1 and a drawdown chart.

## 🚀 Getting Started

```bash
pip install yfinance pandas numpy matplotlib scipy
python etf_momentum_backtest.py
```

## ⚠️ Known Limitations

- **Short history:** `dropna()` trims the data to when the youngest ETF began trading, so the sample may be shorter than 2015 to 2026.
- **Small universe:** six ETFs make results noisy, so a single backtest shouldn't be over-trusted.
- **Sharpe uses a 0% risk-free rate,** which flatters the ratio slightly.
- **Simplified costs:** a flat 5 bps ignores bid-ask spreads, slippage, and taxes.
- **No parameter tuning yet:** the lookback (63) and top-N (3) are fixed, so results may not be robust to other choices.

## 🗺️ Roadmap

- [ ] Wrap the strategy in `run_backtest(lookback, top_n)`
- [ ] Sharpe heatmap across lookbacks (21, 63, 126, 252) and top-N (1, 2, 3)
- [ ] Dual momentum filter: move to cash or TLT when an ETF's momentum is negative
- [ ] Inverse-volatility weighting
- [ ] Walk-forward / out-of-sample split (tune on 2015 to 2020, test on 2021 to 2025)
- [ ] Min-variance / max-Sharpe portfolio via `scipy.optimize` as a comparison strategy
- [ ] Regime analysis (2020 crash, 2022 stock/bond selloff, 2023 to 2025 rally)
