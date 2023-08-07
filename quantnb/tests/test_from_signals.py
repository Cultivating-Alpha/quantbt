from numba import njit
from quantnb.lib.plotting import plotting
from quantnb.lib.time_manip import time_manip
from quantnb.lib import np, timeit, pd, find_files
from quantnb.lib.calculate_stats import calculate_stats
from quantnb.lib.output_trades import output_trades

import quantnb as qnb

from quantnb.strategies.S_base import S_base
from quantnb.core.backtester import Backtester
from quantnb.strategies.S_bid_ask import S_bid_ask
from quantnb.core.place_orders_on_ohlc import place_orders_on_ohlc
import matplotlib

# ==================================================================== #
#                                                                      #
# ==================================================================== #

ohlc = pd.read_parquet("./data/@ENQ-M1.parquet")
ohlc["date"] = time_manip.convert_datetime_to_s(ohlc["time"])

ohlc = ohlc[-100:]
# print(ohlc)


from quantnb.indicators import talib_SMA

sma = talib_SMA(ohlc.close, 20)

ohlc.set_index("time", inplace=True)
entries = qnb.indicators.cross_above(ohlc.close, sma)
exits = qnb.indicators.cross_below(ohlc.close, sma)


def plot():
    plotting.mpf_plot(
        ohlc,
        subplots=[
            plotting.add_line_plot(sma, color="red"),
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
    date=ohlc.date.values,
)
backtester.from_signals(
    long_entries=entries,
    long_exits=exits,
    short_entries=exits,
    short_exits=entries,
    short_entry_price=ohlc.close.to_numpy(dtype=np.float32),
    long_entry_price=ohlc.close.to_numpy(dtype=np.float32),
)


trades = output_trades(backtester.bt, unit="s")
print(trades)
#
# plot()
#
# # |%%--%%| <6DyxzBZE96|jsfBnSWLJE>
#
#
# class TestFromSignals:
#     def was_trade_filled(self, i, date, last_trade, last_trade_index=None, debug=False):
#         a = 5
#         assert a == 5
