from numba import njit
from quantnb.lib.plotting import plotting
from quantnb.lib.time_manip import time_manip
from quantnb.lib import np, timeit, pd, find_files
from quantnb.lib.calculate_stats import calculate_stats
from quantnb.lib.output_trades import output_trades

import quantnb as qnb
import talib

from quantnb.strategies.S_base import S_base
from quantnb.core.backtester import Backtester
from quantnb.strategies.S_bid_ask import S_bid_ask
from quantnb.core.place_orders_on_ohlc import place_orders_on_ohlc
import matplotlib

import quantnb.indicators as ind

# ==================================================================== #
#                                                                      #
# ==================================================================== #

# ohlc = pd.read_parquet("./data/@ENQ-M1.parquet")
# ohlc["Date"] = time_manip.convert_datetime_to_s(ohlc["time"])
ohlc = pd.read_parquet("./data/binance-BTCUSDT-1h.parquet")
ohlc.reset_index(inplace=True)
ohlc

# ohlc = ohlc[-1000:]
print(ohlc)


def get_signals(params):
    long, short, cutoff, atr_distance = params
    close = ohlc.close
    ma_long = ind.SMA(ohlc.close, long)
    ma_short = ind.SMA(close, short)
    rsi = talib.RSI(close, timeperiod=2)
    atr = talib.ATR(ohlc.high, ohlc.low, close, 14)

    entries = np.logical_and(
        close <= ma_short,
        np.logical_and(close >= ma_long, rsi <= cutoff),
    )

    entries = ind.cross_below(close, ma_short)
    # exits = close > ma_short
    exits = ind.cross_above(close, ma_short)

    sl = ohlc.low - atr * atr_distance

    return entries, exits, sl.values, ma_long, ma_short, rsi


params = (123, 11, 13, 2.5)
entries, exits, sl, ma_long, ma_short, rsi = get_signals(params)
entries
exits


# ohlc.set_index("time", inplace=True)


def plot():
    plotting.mpf_plot(
        ohlc,
        subplots=[
            plotting.add_line_plot(ma_long, color="black"),
            plotting.add_line_plot(ma_short, color="blue"),
            plotting.add_line_plot(rsi, panel=1, color="black"),
            plotting.add_markers(
                entries,
                ohlc.close,
                color="green",
                marker_type=matplotlib.markers.CARETUP,
            ),
            plotting.add_markers(
                exits,
                ohlc.close,
                color="red",
                marker_type=matplotlib.markers.CARETDOWNBASE,
            ),
        ],
    )


# files = find_files("./data", "binance-BTCUSD")
# btc = pd.read_parquet(files[0])
# btc
from quantnb.core.enums import DataType


backtester = qnb.core.backtester.Backtester(
    close=ohlc.close.to_numpy(dtype=np.float32),
    data_type=DataType.OHLC,
    date=time_manip.convert_datetime_to_ms(ohlc.Date).values,
    initial_capital=1000000,
)
backtester.from_signals(
    long_entries=entries,
    long_exits=exits,
    short_entries=exits,
    short_exits=entries,
    short_entry_price=ohlc.close,
    long_entry_price=ohlc.close,
)

trades = output_trades(backtester.bt)
trades


ohlc["Date"] = time_manip.convert_s_to_datetime(ohlc["Date"])
stats = calculate_stats(ohlc, backtester.bt)

# equity = backtester.data_module.equity
plotting.plot_equity(backtester, ohlc, "close")
# equity
# equity.plot()
plt.show()
