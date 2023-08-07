from numba import njit
from quantnb.lib.plotting import plotting
from quantnb.lib.time_manip import time_manip
from quantnb.lib import np, timeit, pd, find_files
from quantnb.lib.calculate_stats import calculate_stats
from quantnb.lib.output_trades import output_trades
from quantnb.core.enums import CommissionType, DataType

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
ohlc = pd.read_parquet("./data/binance-BTCUSDT-1h.parquet")
ohlc.reset_index(inplace=True)

"""
Uncomment this if you want to see how it would look like on arbitrum equivalent data, which start in Dec 2022
"""
# ohlc = ohlc[-6000:]

INITIAL_CAPITAL = 10000
ohlc


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


def plot():
    data = ohlc.copy()
    data.set_index("Date", inplace=True)
    plotting.mpf_plot(
        data,
        subplots=[
            plotting.add_line_plot(ma_long, color="black"),
            plotting.add_line_plot(ma_short, color="blue"),
            plotting.add_line_plot(rsi, panel=1, color="black"),
            plotting.add_markers(
                entries,
                data.close,
                color="green",
                marker_type=matplotlib.markers.CARETUP,
            ),
            plotting.add_markers(
                exits,
                data.close,
                color="red",
                marker_type=matplotlib.markers.CARETDOWNBASE,
            ),
        ],
        type="line",
    )


"""
Uncomment this if you want to see the OHLC data with indicators and signals of entries/exits
"""
# plot()


backtester = qnb.core.backtester.Backtester(
    close=ohlc.close.to_numpy(dtype=np.float32),
    data_type=DataType.OHLC,
    date=time_manip.convert_datetime_to_ms(ohlc.Date).values,
    initial_capital=INITIAL_CAPITAL,
    commission=0.0005,
    commission_type=CommissionType.PERCENTAGE,
)

import time

start = time.time()
backtester.from_signals(
    long_entries=entries,
    long_exits=exits,
    short_entries=exits,
    short_exits=entries,
    short_entry_price=ohlc.close,
    long_entry_price=ohlc.close,
)
end = time.time()
print(f"Time taken: {end-start}")

trades, closed_trades, active_trades = output_trades(backtester.bt)
print(trades)


ohlc["Date"] = time_manip.convert_s_to_datetime(ohlc["Date"])
stats = calculate_stats(ohlc, backtester.bt)

# plotting.plot_equity(backtester, ohlc, "close")
