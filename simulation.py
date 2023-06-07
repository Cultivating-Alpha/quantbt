import numpy as np
import pandas as pd
from backtester import backtest

import quantstats as qs
import talib

from temp import SMA, print_trades, plot_equity, calculate_metrics
from plot_ohlc import plot_ohlc


def simulation(data, entries, exists, sl, mode, use_sl):
    close = data.Close
    size = np.full_like(close, 1)
    multiplier = 1
    size = size * multiplier
    # fees = np.full_like(prices, 2.2)

    final_value, total_pnl, equity, orders_array, trades_array = backtest(
        close.values,
        data.Low.values,
        data.Open.values,
        data.index.values.astype(np.int64),
        entries.values,
        exists.values,
        sl.values,
        size,
        initial_capital=10000,
        transaction_cost=0.0005,
        mode=mode,
        use_sl=use_sl,
    )

    return final_value, equity, orders_array, trades_array


def get_signals(data, long, short, cutoff=5, atr_distance=2):
    close = data.Close
    ma_long = SMA(close, long)
    ma_short = SMA(close, short)
    rsi = talib.RSI(close, timeperiod=2)
    atr = talib.ATR(data.High, data.Low, close, 14)

    # entry_signals = ma_long.vbt.crossed_below(ma_short)
    # exit_signals = ma_long.vbt.crossed_above(ma_short)
    # entries = np.logical_and(close >= ma_long, rsi <= cutoff)
    entries = np.logical_and(
        close <= ma_short, np.logical_and(close >= ma_long, rsi <= cutoff)
    )
    exits = close > ma_short
    # exits = rsi > 70

    sl = data.Low - atr * atr_distance
    return entries, exits, ma_long, ma_short, rsi, atr, sl


# |%%--%%| <Lndv6f6cWV|jriB9tCwHI>


####
# data = pd.read_parquet("./data/WBNB-BUSD-h4.parquet")
# data = pd.read_parquet("./data/uniswap-v3-WETH-USDC-h4.parquet")
# data = pd.read_parquet("./data/uniswap_v3-polygon-WETH-USDC-4h.parquet")
# data = data[2:]
# data
# data = pd.read_parquet("./data/uniswap_v3-ethereum-WETH-USDC-4h.parquet")
# data = data[-2000:]
# data
# # data = pd.read_parquet("./data/binance-ETHUSDT.parquet")
# # data = pd.read_parquet("./data/binance-BTCUSDT.parquet")
# # data.drop(columns=["volume"], inplace=True)
# # data.plot()
# # returns = pd.Series(equity, index=data.index)
# # # returns = returns[returns > 100]
# # returns.plot()
# # plt.show()


polygon = pd.read_parquet("./data/uniswap_v3-polygon-WETH-USDC-4h.parquet")
polygon = polygon[2:]

ETH = pd.read_parquet("./data/uniswap_v3-ethereum-WETH-USDC-4h.parquet")
ETH = pd.read_parquet("./data/uniswap_v3-ethereum-WETH-USDC-15m.parquet")
ETH

data = pd.read_parquet("./data/uniswap_v3-polygon-WMATIC-USDC-4h.parquet")
# data =  pd.read_parquet("./data/uniswap_v3-ethereum-WETH-USDC-4h.parquet")
data
# ETH['Close'].plot()
# plt.show()
# ETH = ETH[-1998:]


# polygon = polygon[530:760]
# ETH = ETH[530:760]


data.rename(
    columns={"close": "Close", "high": "High", "low": "Low", "open": "Open"},
    inplace=True,
)
# data = data[500:800]
# data = data[500:]
# data = data[4065:4290]
# data = data[4070:4290]
# data = data[350:580]
data


# data = data.resample("16h").last()


def run(data):
    # entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(data, 200, 10, 5, 1)
    entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(data, 200, 11, 9, 2.5)
    # entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(data, 216, 9, 13, 2)
    # entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(data, 216, 50, 20, 2)
    (final_value, equity, orders_arr, trades_arr) = simulation(
        data, entries, exits, sl, mode=1, use_sl=True
    )

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
    print()
    print()
    # print_trades(trades_arr)
    print()
    print()
    # plot_equity(equity, data)
    # offset = 50
    # plot_ohlc(data[offset:], equity[offset:], entries[offset:], exits[offset:], ma_long[offset:], ma_short[offset:], rsi[offset:], sl[offset:])
    # data

    from Helpers import Helpers

    data.reset_index(inplace=True)
    data.rename(columns={"timestamp": "Date"}, inplace=True)
    data.set_index("Date", inplace=True)

    # Helpers.save_to_csv(data, ma_long, ma_short, rsi, atr, entries, orders_arr, equity, "")
    return equity


# correlation_close = ETH['Close'].corr(polygon['Close'])
# correlation_high = ETH['High'].corr(polygon['High'])
# correlation_low = ETH['Low'].corr(polygon['Low'])
# correlation_open = ETH['Open'].corr(polygon['Open'])
# print(correlation_open)
# print(correlation_high)
# print(correlation_low)
# print(correlation_close)

equity = run(data)
# equity_eth = run(ETH)
# equity_polygon = run(polygon)
#
# pd.Series(equity_eth, index=ETH.index).plot()
# pd.Series(equity_polygon, index=polygon.index).plot()
# polygon['Close'].plot()
# ETH['Close'].plot()
# plt.show()

# |%%--%%| <jriB9tCwHI|3jmGlLWKSo>

# import pandas as pd
# from concurrent.futures import ThreadPoolExecutor
# from tqdm import tqdm
#
#
# def process_entry(long, short, rsi_cutt, atr_distance):
#     # print()
#     # print(
#     #     f"Simulation with long={long}, short={short}, rsi={rsi_cutt}, atr={atr_distance}"
#     # )
#     entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(
#         data, long, short, rsi_cutt, atr_distance
#     )
#     (final_value, equity, orders_arr, trades_arr) = simulation(data, entries, exits, sl)
#     dd, total_return, ratio = calculate_metrics(equity, data, final_value)
#     return {
#         "long": long,
#         "short": short,
#         "rsi": rsi_cutt,
#         "atr": atr_distance,
#         "final_value": final_value,
#         "dd": dd,
#         "total_return": total_return,
#         "ratio": ratio,
#     }
#
#
# values = []
# df = pd.DataFrame()
#
# # Calculate the total number of combinations
# total_combinations = (
#     len(range(200, 300, 1))
#     * len(range(5, 55, 1))
#     * len(range(3, 15, 1))
#     * len(np.arange(0.5, 10.5, 0.5))
# )
#
# # Initialize a progress bar
# pbar = tqdm(total=total_combinations, ncols=80)
#
# with ThreadPoolExecutor(max_workers=max_workers) as executor:
#     results = [
#         executor.submit(process_entry, long, short, rsi_cutt, atr_distance)
#         for long in range(200, 300, 1)
#         for short in range(5, 55, 1)
#         for rsi_cutt in range(3, 15, 1)
#         for atr_distance in np.arange(0.5, 10.5, 0.5)
#     ]
#
#     for result in results:
#         # Update the progress bar
#         pbar.update(1)
#
#         newdf = pd.DataFrame(result.result(), index=[0])
#         df = pd.concat([df, newdf])
#
# # Close the progress bar
# pbar.Close()
#
#
# df = df[df["final_value"] > 12000]
# df.sort_values("final_value", ascending=False, inplace=True)
# df.sort_values("ratio", ascending=False, inplace=True)
# df
# df.tail(50)
# df.to_parquet("./WMATIC-optimisation.parquet")
# # print(df)
# #
# |%%--%%| <3jmGlLWKSo|5wvB9uEcEU>

from tqdm import tqdm


def process_entry(long, short, rsi_cutt, atr_distance):
    entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(
        data, long, short, rsi_cutt, atr_distance
    )
    (final_value, equity, orders_arr, trades_arr) = simulation(
        data, entries, exits, sl, mode=1, use_sl=True
    )
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


total_combinations = (
    len(range(200, 300, 1))
    * len(range(5, 55, 1))
    * len(range(3, 15, 1))
    * len(np.arange(0.5, 10.5, 0.5))
)

pbar = tqdm(total=total_combinations, ncols=80)
i = 0
values = []
df = pd.DataFrame()
for long in range(200, 300, 1):
    for short in range(5, 55, 1):
        for rsi_cutt in range(3, 15, 1):
            for atr_distance in np.arange(0.5, 10.5, 0.5):
                print(f"{i}/{total_combinations}", end="\r")
                i += 1
                result = process_entry(long, short, rsi_cutt, atr_distance)

                # Update the progress bar
                pbar.update(1)
                newdf = pd.DataFrame(result, index=[0])
                df = pd.concat([df, newdf])
        df.to_parquet("./WMATIC-optimisation.parquet")
pbar.close()
df.to_parquet("./WMATIC-optimisation.parquet")


df = df[df["final_value"] > 12000]
df.sort_values("final_value", ascending=False, inplace=True)
df.sort_values("ratio", ascending=False, inplace=True)
df.tail(50)
print(df)


# import pandas as pd
# import numpy as np
# from concurrent.futures import ProcessPoolExecutor
# from tqdm import tqdm
#
#
# def process_entry(args):
#     long, short, rsi_cutt, atr_distance, data = args
#     # Rest of the code...
#
#
# values = []
# df = pd.DataFrame()
#
# # Calculate the total number of combinations
# total_combinations = (
#     len(range(200, 300, 1))
#     * len(range(5, 55, 1))
#     * len(range(3, 15, 1))
#     * len(np.arange(0.5, 10.5, 0.5))
# )
#
# # Set the maximum number of processes
# max_processes = 20
#
# # Initialize a progress bar
# pbar = tqdm(total=total_combinations, ncols=80)
#
# with ProcessPoolExecutor(max_workers=max_processes) as executor:
#     args_list = [
#         (long, short, rsi_cutt, atr_distance, data)
#         for long in range(200, 300, 1)
#         for short in range(5, 55, 1)
#         for rsi_cutt in range(3, 15, 1)
#         for atr_distance in np.arange(0.5, 10.5, 0.5)
#     ]
#
#     results = list(tqdm(executor.map(process_entry, args_list), total=total_combinations))
#
#     for result in results:
#         # Update the progress bar
#         pbar.update(1)
#
#         newdf = pd.DataFrame(result, index=[0])
#         df = pd.concat([df, newdf])
#
# # Close the progress bar
# pbar.close()
#
# df = df[df["final_value"] > 12000]
# df.sort_values("final_value", ascending=False, inplace=True)
# df.sort_values("ratio", ascending=False, inplace=True)
# df.tail(50)
# df.to_parquet("./WMATIC-optimisation.parquet")
#
