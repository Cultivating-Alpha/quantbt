from quantnb.lib.time_manip import time_manip
from quantnb.lib import np, pd, find_files, optimize
from quantnb.lib.plotting import plotting
from quantnb.lib.calculate_stats import calculate_stats
from quantnb.lib.output_trades import output_trades
from quantnb.core.enums import CommissionType, DataType
import time

import quantnb as qnb

# import talib
import pandas_ta as ta

from quantnb.strategies.S_base import S_base
from quantnb.core.backtester import Backtester
from quantnb.strategies.S_bid_ask import S_bid_ask
from quantnb.core.place_orders_on_ohlc import place_orders_on_ohlc
import matplotlib

import quantnb.indicators as ind

import os
from quantnb.lib import np, timeit, pd, find_files


def file_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False


# assets = find_files("./data/", "binance-BTC")
# assets


ohlc = pd.read_parquet("./data/binance-BTCUSDT-1h.parquet")
ohlc.reset_index(inplace=True)

"""
Uncomment this if you want to see how it would look like on arbitrum equivalent data, which start in Dec 2022
"""
# ohlc = ohlc[-6000:]

INITIAL_CAPITAL = 10000
ohlc


def strategy(ohlc, params):
    def get_signals(params):
        # long, short, cutoff, atr_distance = params
        long, short, cutoff = params
        close = ohlc.close
        # ma_long = ind.talib_SMA(ohlc.close, long)
        # ma_short = ind.talib_SMA(close, short)
        # rsi = talib.RSI(close, timeperiod=2)
        # atr = talib.ATR(ohlc.high, ohlc.low, close, 14)

        ma_long = ta.sma(ohlc.close, length=long)
        ma_short = ta.sma(ohlc.close, length=short)
        rsi = ta.rsi(ohlc.close, length=2)
        atr = ta.atr(ohlc.high, ohlc.low, close, 14)
        #
        entries = np.logical_and(
            close <= ma_short,
            np.logical_and(close >= ma_long, rsi <= cutoff),
        ).values
        exits = ind.cross_above(close, ma_short)

        # sl = ohlc.low - atr * atr_distance

        return entries, exits, ma_long, ma_short, rsi

    entries, exits, ma_long, ma_short, rsi = get_signals(params)
    backtester = qnb.core.backtester.Backtester(
        close=ohlc.close.to_numpy(dtype=np.float32),
        data_type=DataType.OHLC,
        date=time_manip.convert_datetime_to_ms(ohlc["Date"]).values,
        initial_capital=INITIAL_CAPITAL,
        commission=0.0005,
        commission_type=CommissionType.PERCENTAGE,
    )

    # Shift the array one position to the left
    def shift(arr, index=1):
        return np.concatenate((arr[index:], arr[:index]))

    start = time.time()
    backtester.from_signals(
        long_entries=entries,
        long_exits=exits,
        short_entries=exits,
        short_exits=entries,
        short_entry_price=shift(ohlc.open),
        long_entry_price=shift(ohlc.open),
        # short_entry_price=ohlc.close.to_numpy(dtype=np.float32),
        # long_entry_price=ohlc.close.to_numpy(dtype=np.float32),
    )

    trades, closed_trades, active_trades = output_trades(backtester.bt)
    trades.drop(
        columns=["IDX", "Index", "Direction", "CloseReason", "Extra", "SL", "TIME_SL"],
        inplace=True,
    )
    stats = calculate_stats(
        ohlc,
        trades,
        closed_trades,
        backtester.data_module.equity,
        INITIAL_CAPITAL,
        display=False,
        index=[(params)],
    )
    plotting.plot_equity(backtester, ohlc, "close")
    return stats


# for i in range(0, 1):
#     for long in range(100 + i * 50, 150 + i * 50, 1):
#         for short in range(5, 55, 1):
#             for rsi in range(3, 15, 1):
#                 stats = strategy(ohlc, (long, short, rsi))
#                 print(stats)

ohlc

params = (163, 29, 7)
strategy(ohlc, params)

# |%%--%%| <QgQzeXd36C|B71b17sxwt>


assets = find_files("./data/", "binance-BTC")
for asset in assets:
    sym = asset.split("/")[-1].split(".")[0]
    data = pd.read_parquet(asset)
    data = ohlc
    sym = "BTCUSDT"
    print(asset)
    print(data)
    for i in range(0, 9):
        print(i)
        out = f"./optimisation/{sym}-RSI-{i}.parquet"
        if not file_exists(out):
            optimisation = optimize(
                ohlc,
                strategy,
                # long=range(100, 101, 1),
                # short=range(5, 55, 1),
                # rsi=range(3, 15, 1),
                long=range(100 + i * 50, 150 + i * 50, 1),
                short=range(5, 55, 1),
                rsi=range(3, 15, 1),
                # atr_distance=np.arange(0.5, 10.5, 0.5),
            )
            print(optimisation)
            # optimisation = optimisation.sort_values("ratio", ascending=False)
            optimisation.to_parquet(f"./optimisation/{sym}-RSI-{i}.parquet")
# print(optimisation)
# optimisation = optimisation.sort_values("ratio", ascending=False)
# optimisation.to_parquet(f"./optimisation/BTCUSDT-RSI-{0}.parquet")
# |%%--%%| <B71b17sxwt|pWx5QqDRAd>


optiz = find_files("./optimisation/", "BTC")
optiz
df = pd.DataFrame()
for opti in optiz:
    newdf = pd.read_parquet(opti)
    df = pd.concat([df, newdf])

df

df = df[df["ratio"] > 3]
df = df.sort_values("DD", ascending=True)
df
