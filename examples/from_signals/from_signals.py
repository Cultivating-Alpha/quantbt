from numba import njit
from quantnb.lib.plotting import plotting
from quantnb.lib.time_manip import time_manip
from quantnb.lib import np, timeit, pd, find_files
from quantnb.lib.calculate_stats import calculate_stats
from quantnb.lib.output_trades import output_trades
from quantnb.core.enums import CommissionType, DataType
from quantnb.lib import pd, find_files, np, optimize

import quantnb as qnb

# import talib
import pandas_ta as ta

from quantnb.strategies.S_base import S_base
from quantnb.core.backtester import Backtester
from quantnb.strategies.S_bid_ask import S_bid_ask
from quantnb.core.place_orders_on_ohlc import place_orders_on_ohlc
import matplotlib

import quantnb.indicators as ind

# ==================================================================== #
#                                                                      #
# ==================================================================== #
ohlc = pd.read_parquet("./data/binance-BTCUSDT-1h.parquet")
ohlc.reset_index(inplace=True)

"""
Uncomment this if you want to see how it would look like on arbitrum equivalent data, which start in Dec 2022
"""
# ohlc = ohlc[-6000:]

INITIAL_CAPITAL = 10000
ohlc

# ohlc = ohlc[0:210]

# ohlc = ohlc[3120:4600]
ohlc = ohlc[3120:]
ohlc


# def get_signals(params):
#     # long, short, cutoff, atr_distance = params
#     long, short, cutoff = params
#     close = ohlc.close
#     # ma_long = ind.talib_SMA(ohlc.close, long)
#     # ma_short = ind.talib_SMA(close, short)
#     # rsi = talib.RSI(close, timeperiod=2)
#     # atr = talib.ATR(ohlc.high, ohlc.low, close, 14)
#
#     ma_long = ta.sma(ohlc.close, length=long)
#     ma_short = ta.sma(ohlc.close, length=short)
#     rsi = ta.rsi(ohlc.close, length=2)
#     atr = ta.atr(ohlc.high, ohlc.low, close, 14)
#     #
#     entries = np.logical_and(
#         close <= ma_short,
#         np.logical_and(close >= ma_long, rsi <= cutoff),
#     ).values
#     exits = ind.cross_above(close, ma_short)
#
#     # sl = ohlc.low - atr * atr_distance
#
#     return entries, exits, ma_long, ma_short, rsi
#
#
# # params = (123, 11, 10, 2.5)
# params = (112, 6, 8)
# entries, exits, ma_long, ma_short, rsi = get_signals(params)
#
#
# def plot():
#     data = ohlc.copy()
#     data.set_index("Date", inplace=True)
#     plotting.mpf_plot(
#         data,
#         subplots=[
#             plotting.add_line_plot(ma_long, color="black"),
#             plotting.add_line_plot(ma_short, color="blue"),
#             plotting.add_line_plot(rsi, panel=1, color="black"),
#             plotting.add_markers(
#                 entries,
#                 data.close,
#                 color="green",
#                 marker_type=matplotlib.markers.CARETUP,
#             ),
#             plotting.add_markers(
#                 exits,
#                 data.close,
#                 color="red",
#                 marker_type=matplotlib.markers.CARETDOWNBASE,
#             ),
#         ],
#         type="line",
#     )
#
#
# """
# Uncomment this if you want to see the OHLC data with indicators and signals of entries/exits
# """
# # plot()
#
# backtester = qnb.core.backtester.Backtester(
#     close=ohlc.close.to_numpy(dtype=np.float32),
#     open=ohlc.open.to_numpy(dtype=np.float32),
#     high=ohlc.high.to_numpy(dtype=np.float32),
#     low=ohlc.low.to_numpy(dtype=np.float32),
#     data_type=DataType.OHLC,
#     date=time_manip.convert_datetime_to_ms(ohlc.Date).values,
#     initial_capital=INITIAL_CAPITAL,
#     commission=0.0005,
#     commission_type=CommissionType.PERCENTAGE,
# )
#
# import time
#
#
# # Shift the array one position to the left
# def shift(arr, index=-1):
#     return np.concatenate((arr[index:], arr[:index]))
#
# # ohlc.open
# # shift(ohlc.open, -1)
#
# start = time.time()
# backtester.from_signals(
#     long_entries=entries,
#     long_exits=exits,
#     short_entries=exits,
#     short_exits=entries,
#     long_entry_price=shift(ohlc.open, index=1),
#     short_entry_price=shift(ohlc.open, index=1),
#     # short_entry_price=ohlc.close.to_numpy(dtype=np.float32),
#     # long_entry_price=ohlc.close.to_numpy(dtype=np.float32),
# )
# end = time.time()
# # print(f"Time taken: {end-start}")
# print()
# print()
#
# trades, closed_trades, active_trades = output_trades(backtester.bt)
# trades.drop(
#     columns=["IDX", "Index", "Direction", "CloseReason", "Extra", "SL", "TIME_SL", "Active", "TP", "SL"],
#     inplace=True,
# )
#
#
# ohlc["Date"] = time_manip.convert_s_to_datetime(ohlc["Date"])
#
# bt = backtester
# stats = calculate_stats(
#     ohlc,
#     trades,
#     closed_trades,
#     bt.data_module.equity,
#     INITIAL_CAPITAL,
#     display=False,
#     index=[(params)],
# )
#
# #
# # plotting.plot_equity(backtester, ohlc, "close")
# stats
# # trades[0:5]
#
# #|%%--%%| <R24nG346eC|wPh8Xau8CI>
#
# test = pd.DataFrame()
# test['Com'] = trades['EntryPrice'] * trades['Volume'] * 0.0005 + trades['ExitPrice'] * trades['Volume'] * 0.0005 
# test['PnL'] = (trades['ExitPrice'] - trades['EntryPrice']) * trades['Volume'] - test['Com']
# test['PnL'].sum()
# trades['PNL'].sum()
# test
#
# test['Com']
# trades['Commission']

#|%%--%%| <wPh8Xau8CI|jCpl1Zdnkj>


ts = pd.read_parquet('./data/ts.parquet')
ts

trades
diff = pd.DataFrame({'diff': ts['PnL'].values - trades['PNL'].values})
ts['PnL']
trades['PNL']

diff.sum()
diff.plot()
plt.show(0)
#
# ts
#
trades
diff = pd.DataFrame({'diff': ts['Entry mid price'].values - trades['EntryPrice'].values})
diff = pd.DataFrame({'diff': ts['Exit mid price'].values - trades['ExitPrice'].values})
diff
# trades['PNL'].sum()
#
#|%%--%%| <jCpl1Zdnkj|bKsjcb3XDl>

print(trades[0:5])

start = 302
end = 700
entries[start:end]
ohlc[start:end].head()

df = ohlc[start:end].copy()
df['entries']=entries[start:end]
df['ma'] = ma_short[start:end]
df['ma_long'] = ma_long[start:end]
df['rsi'] = rsi[start:end]
df.head()


# |%%--%%| <bKsjcb3XDl|QgQzeXd36C>

import os
from quantnb.lib import np, timeit, pd, find_files

def strategy(ohlc, params, plot=False):
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

    backtester.from_signals(
        long_entries=entries,
        long_exits=exits,
        short_entries=exits,
        short_exits=entries,
        short_entry_price=shift(ohlc.open),
        long_entry_price=shift(ohlc.open),
        # short_entry_price=ohlc.close.to_numpy(dtype=np.float32),
        # long_entry_price=ohlc.close.to_numpy(dtype=np.float32),
        default_size=0.99
    )
    trades, closed_trades, active_trades = output_trades(backtester.bt)
    stats = calculate_stats(
        ohlc,
        trades,
        closed_trades,
        backtester.data_module.equity,
        INITIAL_CAPITAL,
        display=False,
        index=[(params)],
    )
    print(stats)
    if plot:
        plotting.plot_equity(backtester, ohlc, "close")
    return stats


strategy(ohlc, (112, 6, 8), plot=True)
strategy(ohlc, (526, 6, 10), plot=True)
# for i in range(0, 1):
#     for long in range(100 + i * 50, 150 + i * 50, 1):
#         for short in range(5, 55, 1):
#             for rsi in range(3, 15, 1):
#                 stats = strategy(ohlc, (long, short, rsi))

# |%%--%%| <QgQzeXd36C|B71b17sxwt>


assets = find_files("./data/", "binance-BTC")
assets

step = 50
for asset in assets:
    sym = asset.split("/")[-1].split(".")[0]
    data = pd.read_parquet(asset)
    print(asset)
    print(data)
    for i in range(0, 9):
        print(i)
        out = f"./optimisation/{sym}-RSI-{i}.parquet"
        if not os.path.exists(out):
            optimisation = optimize(
                ohlc,
                strategy,
                # long=range(100, 101, 1),
                # short=range(5, 55, 1),
                # rsi=range(3, 15, 1),
                long=range(100 + i * step, 150 + i * step, 1),
                short=range(5, 55, 1),
                rsi=range(3, 15, 1),
                # atr_distance=np.arange(0.5, 10.5, 0.5),
            )
            print(optimisation)
            # optimisation = optimisation.sort_values("ratio", ascending=False)
            optimisation.to_parquet(f"./optimisation/{sym}-RSI-{i}.parquet")
# print(optimisation)
# optimisation.sort_values("ratio", ascending=False)
# |%%--%%| <B71b17sxwt|wKaYjtFVdf>


newdf = pd.DataFrame()

opti = find_files("./optimisation/", "RSI")
for opt in opti:
    df = pd.read_parquet(opt)
    newdf = pd.concat([newdf, df])

# newdf.sort_values("RIO: (%)", ascending=False)
newdf.sort_values("ratio", ascending=False)
newdf.sort_values("End Value", ascending=False)
