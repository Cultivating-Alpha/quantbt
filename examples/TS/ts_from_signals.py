from numba import njit
from quantbt.lib.plotting import plotting
from quantbt.lib.time_manip import time_manip
from quantbt.lib import np, timeit, pd, find_files
from quantbt.lib.calculate_stats import calculate_stats
from quantbt.lib.output_trades import output_trades
from quantbt.core.enums import CommissionType, DataType, TradeSizeType
from quantbt.lib import pd, find_files, np, optimize
from quantbt.lib.data_to_csv import save_data

import quantbt as qnb

# import talib
import pandas_ta as ta

from quantbt.strategies.S_base import S_base
from quantbt.core.backtester import Backtester
from quantbt.strategies.S_bid_ask import S_bid_ask
from quantbt.core.place_orders_on_ohlc import place_orders_on_ohlc
import matplotlib

import quantbt.indicators as ind

# ==================================================================== #
#                                                                      #
# ==================================================================== #
eth = pd.read_parquet("./data/binance-ETHUSDT-1h.parquet")
btc = pd.read_parquet("./data/binance-BTCUSDT-1h.parquet")
btc.reset_index(inplace=True)
eth.reset_index(inplace=True)


"""
Uncomment this if you want to see how it would look like on arbitrum equivalent data, which start in Dec 2022
"""
# ohlc = ohlc[-6000:]

INITIAL_CAPITAL = 10000
# ohlc = ohlc[3120:]
# ohlc = ohlc[38222:]


# |%%--%%| <bKsjcb3XDl|pkuzKHVZ2t>

import os
from quantbt.lib import np, timeit, pd, find_files
#
# def strategy(ohlc, params, plot=False):
#     def get_signals(params):
#         # long, short, cutoff, atr_distance = params
#         long, short, cutoff = params
#         close = ohlc.close
#         # ma_long = ind.talib_SMA(ohlc.close, long)
#         # ma_short = ind.talib_SMA(close, short)
#         # rsi = talib.RSI(close, timeperiod=2)
#         # atr = talib.ATR(ohlc.high, ohlc.low, close, 14)
#
#         ma_long = ta.sma(ohlc.close, length=long)
#         ma_short = ta.sma(ohlc.close, length=short)
#         rsi = ta.rsi(ohlc.close, length=2)
#         atr = ta.atr(ohlc.high, ohlc.low, close, 14)
#         #
#         entries = np.logical_and(
#             close <= ma_short,
#             np.logical_and(close >= ma_long, rsi <= cutoff),
#         ).values
#         exits = ind.cross_above(close, ma_short)
#
#         # sl = ohlc.low - atr * atr_distance
#
#         return entries, exits, ma_long, ma_short, rsi
#
#     entries, exits, ma_long, ma_short, rsi = get_signals(params)
#     backtester = qnb.core.backtester.Backtester(
#         close=ohlc.close.to_numpy(dtype=np.float32),
#         data_type=DataType.OHLC,
#         date=time_manip.convert_datetime_to_ms(ohlc["Date"]).values,
#         initial_capital=INITIAL_CAPITAL,
#         commission=0.0005,
#         commission_type=CommissionType.PERCENTAGE,
#     )
#
#     # Shift the array one position to the left
#     def shift(arr, index=1):
#         return np.concatenate((arr[index:], arr[:index]))
#
#     backtester.from_signals(
#         long_entries=entries,
#         long_exits=exits,
#         short_entries=exits,
#         short_exits=entries,
#         short_entry_price=shift(ohlc.open),
#         long_entry_price=shift(ohlc.open),
#         long_exit_price=shift(ohlc.open),
#         short_exit_price=shift(ohlc.open),
#         # short_entry_price=ohlc.close.to_numpy(dtype=np.float32),
#         # long_entry_price=ohlc.close.to_numpy(dtype=np.float32),
#     )
#     trades, closed_trades, active_trades = output_trades(backtester.bt)
#     stats = calculate_stats(
#         ohlc,
#         trades,
#         closed_trades,
#         backtester.data_module.equity,
#         INITIAL_CAPITAL,
#         display=False,
#         index=[(params)],
#     )
#     print(stats)
#     if plot:
#         plotting.plot_equity(backtester, ohlc, "close")
#     return stats
#
# strategy(ohlc, (526, 6, 10), plot=True)





def strategy(data, params, plot=False):

    class S_signals(S_base):
        def generate_signals(self):
            long, short, cutoff = params
            close = self.data.Close
            high = self.data.High
            low = self.data.Low

            self.ma_long = ta.sma(close, length=long)
            self.ma_short = ta.sma(close, length=short)
            self.rsi = ta.rsi(close, length=2)
            atr = ta.atr(high, low, close, 14)
            #
            entries = np.logical_and(
                close <= self.ma_short,
                np.logical_and(close >= self.ma_long, self.rsi <= cutoff),
            ).values
            exits = ind.cross_above(close, self.ma_short)

            self.long = entries
            self.short = exits

            return {
                'long_entries' : entries,
                'long_exits' : exits,
                # 'long_entries' : np.full(self.long.shape, False),
                # 'long_exits' : np.full(self.long.shape, False),
                'short_entries' : np.full(self.long.shape, False),
                'short_exits' : np.full(self.long.shape, False),
            }

    st = S_signals(
      data, 
      commission=0.0005,
      commission_type=CommissionType.PERCENTAGE,
      multiplier=1,
      data_type=DataType.OHLC,
      initial_capital=10_000,
      default_trade_size=0.99,
      trade_size_type=TradeSizeType.PERCENTAGE,
    )


    st.from_signals(params)

    if plot:
        st.plot_equity()
        trades = st.trades()
        trades.drop(["Active", "IDX", "TIME_SL", "SL", "TP", "Direction", "CloseReason", "Extra"], inplace=True, axis=1)

    return st.stats()

params = (656, 10, 3)

ohlc = btc[38222:]
data = ohlc
stats = strategy(data, params, plot=True)


# |%%--%%| <pkuzKHVZ2t|B71b17sxwt>


assets = find_files("./data/", "binance-BTC")
assets

ohlc = eth[38222:]
ohlc = btc[38222:]

STEP_LONG = 50
STEP_SHORT = 55
STEP_RSI = 15
# STEP_LONG = 50
# STEP_SHORT = 55
# STEP_RSI = 15

sym = "ETH"
for i in range(0, 12):
    print(i)
    out = f"./optimisation/{sym}-RSI-{i}.parquet"
    if not os.path.exists(out):
        optimisation = optimize(
            ohlc,
            strategy,
            long=range(50 + i * STEP_LONG, 100 + i * STEP_LONG, 1),
            short=range(5, STEP_SHORT, 1),
            rsi=range(3, STEP_RSI, 1),
            # atr_distance=np.arange(0.5, 10.5, 0.5),
        )
        print(optimisation)
        # optimisation = optimisation.sort_values("ratio", ascending=False)
        optimisation.to_parquet(f"./optimisation/{sym}-RSI-{i}.parquet")


# print(optimisation)
# optimisation.sort_values("ratio", ascending=False)
# |%%--%%| <B71b17sxwt|8eA7Xk4pw8>

import pandas as pd
from quantbt.lib import find_files


newdf = pd.DataFrame()

btc = find_files("./optimisation/", "BTCUSDT")
eth = find_files("./optimisation/", "ETH-RSI")
for opt in eth:
    df = pd.read_parquet(opt)
    newdf = pd.concat([newdf, df])

newdf = newdf.sort_values("ratio", ascending=False)
# newdf.to_parquet("./optimisation/full-BTC-RSI.parquet")
newdf.to_parquet("./optimisation/full-ETH-RSI.parquet")


#|%%--%%| <8eA7Xk4pw8|CPzWQlSzQZ>

eth_full = pd.read_parquet("./optimisation/full-ETH-RSI.parquet")
btc_full = pd.read_parquet("./optimisation/full-BTC-RSI.parquet")

eth_full
btc_full

#|%%--%%| <CPzWQlSzQZ|Ufsl8mlq0u>


def save_to_csv(data, st):
    """
    Create the dataframes needed for the UI
    """
    df = pd.DataFrame({
        'date': data['Date'],
        'open': data.open,
        'high': data.high,
        'low': data.low,
        'close': data.close,
        'long': st.long,
        'short': st.short,
        'equity': st.bt.data_module.equity
    })
    time_manip.convert_datetime_to_ms(data['Date'])

    # Apply the function to create the new column


    # rsi_scatter_high = data['high']
    # rsi_scatter_low = data['high']

    indicators_data = pd.DataFrame({
        'ma1': st.ma_long,
        'ma2': st.ma_short,
        'equity': st.bt.data_module.equity
    })

    """
    Create the configuration that tells the UI which indicators to draw
    """
    indicators = [{
        "name": "EMA Long",
        "type": "line",
        "panel": 0,
        "dataIndex": 0
      }, {
        "name": "MA Short",
        "type": "line",
        'color': "black",
        "panel": 0,
        "dataIndex": 1
      }, {
        "name": "Equity",
        "type": "line",
        'color': "black",
        "panel": 1,
        "dataIndex": 2
      }
    ]


    """
    Save the data and config to the location of the UI
    """
    UI_LOCATION = "/home/alpha/workspace/cultivating-alpha/candles-ui/public"

    save_data(UI_LOCATION, df, indicators, indicators_data)

save_to_csv(data, st)
