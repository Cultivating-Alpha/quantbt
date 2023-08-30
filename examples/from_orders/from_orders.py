from numba import njit
from quantbt.lib.plotting import plotting
from quantbt.lib import np, timeit, pd
from quantbt.strategies.S_base import S_base
from quantbt.core.backtester import Backtester
from quantbt.strategies.S_bid_ask import S_bid_ask
from quantbt.core.place_orders_on_ohlc import place_orders_on_ohlc

# ==================================================================== #
#                        Default Preparation                           #
# ==================================================================== #
bt = Backtester(commissions=0.002, initial_capital=100000)

VOLUME_MULTIPLIER = 10000

# ==================================================================== #
#                                                                      #
# ==================================================================== #

ohlc = pd.read_parquet("./data/EURUSD.parquet")
orders = pd.read_parquet("./data/sorted_orders.parquet")
orders.loc[orders["direction"] == 0, "volume"] *= -1
# print(orders)
orders_against = pd.read_parquet("./data/sorted_orders_against.parquet")
orders_against.loc[orders_against["direction"] == 0, "volume"] *= -1
# print(orders_against)
# orders
data = ohlc[0:1600000]
# data = ohlc

# data = ohlc[0:1000000]

data = ohlc[0:1000000]


def backtest(data, orders):
    bt = Backtester(commissions=0.002, initial_capital=100000)
    # data = ohlc[615000:626000]
    # data = ohlc
    data, orders_data_array = place_orders_on_ohlc(
        data, orders, "EURUSD.bid", "EURUSD.ask"
    )

    bt.set_bid_ask_data(data["Date"].values, data["Bid"].values, data["Ask"].values)
    bt.from_orders(orders_data_array[:, 1])

    df = plotting.plot_equity(bt.equity, data)
    return df


df = backtest(data, orders)
# df = backtest(data, orders_against)


# |%%--%%| <NarXB5wS7A|fOaSUABOzG>
