import numpy as np
import pandas as pd
from backtester import backtest

import quantstats as qs
import talib

from helpers import SMA, print_trades, plot_equity, calculate_metrics
from plot_ohlc import plot_ohlc


def simulation(data, entries, exists, sl):
    close = data.close
    size = np.full_like(close, 1)
    multiplier = 1
    size = size * multiplier
    # fees = np.full_like(prices, 2.2)

    final_value, total_pnl, equity, orders_array, trades_array = backtest(
        close.values,
        data.index.values.astype(np.int64),
        entries.values,
        exists.values,
        sl.values,
        size,
        initial_capital=10000,
        transaction_cost=0.0002,
    )

    return final_value, equity, orders_array, trades_array


def get_signals(data, long, short, cutoff=5, atr_distance=2):
    close = data.close
    ma_long = SMA(close, long)
    ma_short = SMA(close, short)
    rsi = talib.RSI(close, timeperiod=2)
    atr = talib.ATR(data.high, data.low, close, 14)

    # entry_signals = ma_long.vbt.crossed_below(ma_short)
    # exit_signals = ma_long.vbt.crossed_above(ma_short)
    entries = np.logical_and(close >= ma_long, rsi <= cutoff)
    exits = close > ma_short
    # exits = rsi > 70

    sl = data.low - atr * atr_distance
    return entries, exits, ma_long, ma_short, rsi, atr, sl


####
# data = pd.read_parquet("./data/WBNB-BUSD-h4.parquet")
# data = pd.read_parquet("./data/uniswap-v3-WETH-USDC-h4.parquet")
data = pd.read_parquet("./data/binance-ETHUSDT.parquet")
data = pd.read_parquet("./data/binance-BTCUSDT.parquet")
# data = data[350:850]


import time

start = time.time()
entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(data, 211, 7, 13, 2)
(final_value, equity, orders_arr, trades_arr) = simulation(data, entries, exits, sl)
end = time.time()

#####
dd, total_return, ratio = calculate_metrics(equity, data, final_value)

newdf = pd.DataFrame(
    {
        "final_value": final_value,
        "dd": dd,
        "total_return": total_return,
        "ratio": ratio,
    },
    index=[0],
)
print(newdf)
# print_trades(trades_arr)
# plot_equity(equity, data)
# plot_ohlc(data, equity, entries, exits, ma_long, ma_short, rsi, data.low - atr * 2)

# |%%--%%| <9WGKo4wgwY|3jmGlLWKSo>

import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def process_entry(long, short, rsi_cutt, atr_distance):
    # print()
    # print(
    #     f"Simulation with long={long}, short={short}, rsi={rsi_cutt}, atr={atr_distance}"
    # )
    entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(
        data, long, short, rsi_cutt, atr_distance
    )
    (final_value, equity, orders_arr, trades_arr) = simulation(data, entries, exits, sl)
    dd, total_return, ratio = calculate_metrics(equity, data, final_value)
    return {
        "long": long,
        "short": short,
        "rsi": rsi_cutt,
        "atr": atr_distance,
        "final_value": final_value,
        "dd": dd,
        "total_return": total_return,
        "ratio": ratio,
    }


values = []
df = pd.DataFrame()

# Calculate the total number of combinations
total_combinations = (
    len(range(200, 300, 1))
    * len(range(5, 55, 1))
    * len(range(3, 15, 1))
    * len(np.arange(0.5, 10.5, 0.5))
)

# Initialize a progress bar
pbar = tqdm(total=total_combinations, ncols=80)

with ThreadPoolExecutor(max_workers=1) as executor:
    results = [
        executor.submit(process_entry, long, short, rsi_cutt, atr_distance)
        for long in range(200, 300, 1)
        for short in range(5, 55, 1)
        for rsi_cutt in range(3, 15, 1)
        for atr_distance in np.arange(0.5, 10.5, 0.5)
    ]

    for result in results:
        # Update the progress bar
        pbar.update(1)

        newdf = pd.DataFrame(result.result(), index=[0])
        df = pd.concat([df, newdf])

# Close the progress bar
pbar.close()


df = df[df["final_value"] > 12000]
df.sort_values("final_value", ascending=False, inplace=True)
df.sort_values("ratio", ascending=False, inplace=True)
df
df.tail(50)
df.to_parquet("./optimisation.parquet")
print(df)
#
# # |%%--%%| <3jmGlLWKSo|NUhC9KfUv2>
qs.extend_pandas()
annual_rf_rate = 0.05
rf_rate = (1 + annual_rf_rate) ** (1 / (252 * 60)) - 1
# show sharpe ratio
prices = data.close
returns = pd.Series(equity, index=data.index).pct_change()
returns.sharpe(rf=rf_rate)
# pf.stats(settings=dict(risk_free=rf_rate))
# qs.stats.sharpe(returns, rf=rf_rate)
# pf.plot().show()
# qs.plots.snapshot(stock, title="Facebook Performance")
# # or using extend_pandas() :)

qs.reports.metrics(returns=returns, benchmark=prices, rf=rf_rate)
# (7528.5 - 7545.75) * 2
# qs.reports.html(
#     returns, mode="full", benchmark=prices, output="my_report.html", rf=rf_rate
# )
# final_value
