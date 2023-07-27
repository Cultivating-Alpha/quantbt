from numba import njit
from quantnb.lib.plotting import plotting
from quantnb.lib.time_manip import time_manip
from quantnb.lib import np, timeit, pd
from quantnb.lib.calculate_stats import calculate_stats
from quantnb.lib.output_trades import output_trades
from quantnb.strategies.S_base import S_base
from quantnb.core.backtester import Backtester
from quantnb.strategies.S_bid_ask import S_bid_ask
from quantnb.core.place_orders_on_ohlc import place_orders_on_ohlc

# ==================================================================== #
#                                                                      #
# ==================================================================== #


def get_ohlc_trades():
    ohlc = pd.read_parquet("./data/EURUSD.parquet")
    ohlc.reset_index(inplace=True)

    long = pd.read_parquet("./data/long_trades.parquet")
    long.sort_values(by="long_entry", inplace=True)
    long["direction"] = 1
    short = pd.read_parquet("./data/short_trades.parquet")
    short.sort_values(by="short_entry", inplace=True)
    return long, short, ohlc


long, short, ohlc = get_ohlc_trades()


data = ohlc[0:314000]
data = ohlc[0:1314000]
data = ohlc
data
# data = ohlc[0:1000]
# data
trades = long
# trades
test = time_manip.convert_ms_to_datetime(trades["long_entry"])
test_exit = time_manip.convert_ms_to_datetime(trades["long_exit"])
test
test_exit


# long
long["volume"] = long["volume"] * 100000


def backtest(data, trades):
    bt = Backtester(commissions=0.002, initial_capital=100000)
    # data = ohlc[615000:626000]
    # data = ohlc

    bt.set_bid_ask_data(
        time_manip.convert_datetime_to_ms(data["Date"]).values,
        data["EURUSD.bid"].values,
        data["EURUSD.ask"].values,
    )

    bt.from_trades(trades.values)

    return bt


bt = backtest(data, long)
#
# trades = output_trades(bt)
# trades["ExitPrice"]

# plotting.plot_equity(bt.equity, data, "EURUSD.bid")
# bt, df = backtest(data, short)
# tr = bt.trades
# plotting.plot_equity(bt.equity, data, "EURUSD.bid")
# bt.equity
# |%%--%%| <xxALjYrrlf|vE79q6AEOa>

from quantnb.lib.calculate_stats import calculate_stats

calculate_stats(data, bt)
trades = output_trades(bt)
