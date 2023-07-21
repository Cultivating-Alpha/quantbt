from numba import njit
from quantnb.lib.plotting import plotting
from quantnb.lib import np, timeit, pd
from quantnb.strategies.S_base import S_base
from quantnb.core.backtester import Backtester
from quantnb.strategies.S_bid_ask import S_bid_ask
from quantnb.core.place_orders_on_ohlc import place_orders_on_ohlc

# ==================================================================== #
#                                                                      #
# ==================================================================== #

ohlc = pd.read_parquet("./data/EURUSD.parquet")
ohlc.reset_index(inplace=True)

long_trades = pd.read_parquet("./data/long_trades.parquet")
short_trades = pd.read_parquet("./data/long_trades.parquet")

long_trades

data = ohlc[0:1000000]
trades = long_trades

# |%%--%%| <NarXB5wS7A|fOaSUABOzG>


def backtest(data, trades):
    bt = Backtester(commissions=0.002, initial_capital=100000)
    # data = ohlc[615000:626000]
    # data = ohlc

    bt.set_bid_ask_data(
        data["Date"].values, data["EURUSD.bid"].values, data["EURUSD.ask"].values
    )
    bt.from_trades(trades.values)

    # df = plotting.plot_equity(bt.equity, data, "EURUSD.bid")
    return bt, df


bt, df = backtest(data, long_trades)

bt.equity
