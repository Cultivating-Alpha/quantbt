from numba import njit
from Helpers import Helper
from quantnb.lib import np, timeit, pd
from quantnb.strategies.S_base import S_base
from quantnb.core.backtester import Backtester
from quantnb.strategies.S_bid_ask import S_bid_ask
from place_orders_on_ohlc import place_orders_on_ohlc

# ==================================================================== #
#                        Default Preparation                           #
# ==================================================================== #
helper = Helper()
bt = Backtester(commissions=0.002, initial_capital=100000)

VOLUME_MULTIPLIER = 10000

# ==================================================================== #
#                                                                      #
# ==================================================================== #

ohlc = pd.read_parquet("./data/EURUSD.parquet")
orders = pd.read_parquet("./data/sorted_orders.parquet")

# Make sure volume is negative when orders is short
orders.loc[orders["direction"] == 0, "volume"] *= -1
orders["volume"] *= VOLUME_MULTIPLIER
orders


#
data = ohlc[0:296000]
data = ohlc
data, orders_data_array = place_orders_on_ohlc(data, orders)

bt.set_bid_ask_data(data["Date"].values, data["Bid"].values, data["Ask"].values)


bt.from_orders(orders_data_array[:, 1])

df = helper.plot_equity(bt.equity, data)
