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
orders.loc[orders["direction"] == 0, "volume"] *= -1
# print(orders)
orders_against = pd.read_parquet("./data/sorted_orders_against.parquet")
orders_against.loc[orders_against["direction"] == 0, "volume"] *= -1
# print(orders_against)
# orders
data = ohlc[0:1600000]
# data = ohlc

# data = ohlc[0:1000000]


def backtest(data, orders):
    bt = Backtester(commissions=0.002, initial_capital=100000)
    # data = ohlc[615000:626000]
    # data = ohlc
    data, orders_data_array = place_orders_on_ohlc(data, orders)

    bt.set_bid_ask_data(data["Date"].values, data["Bid"].values, data["Ask"].values)
    bt.from_orders(orders_data_array[:, 1])

    df = helper.plot_equity(bt.equity, data)
    return df


df = backtest(data, orders)
# df = backtest(data, orders_against)


# |%%--%%| <NarXB5wS7A|nh7dvDieEW>


data
test = data.copy()
test["Date"] = pd.to_datetime(test["Date"], unit="ms")
test
test.set_index("Date", inplace=True)
test["Bid"].plot()

# |%%--%%| <nh7dvDieEW|tuOF7yATJd>


# test = test["Bid"].resample("1h").ohlc()

# test["open"].iloc[2] - test["close"].iloc[0]
# test

import mplfinance as mpf


OHLC = test["Bid"].resample("1min").ohlc()

EQUITY = pd.DataFrame(
    {"Equity": bt.equity, "Volume": orders_data_array[:, 1]},
    index=helper.convert_ms_to_datetime(bt.date),
)
OHLC["volume"] = EQUITY["Volume"].resample("1min").last()

EQUITY = EQUITY["Equity"].resample("1min").ohlc()
EQUITY
# orders
#
#
OHLC["volume"][OHLC["volume"] > 10]
# mpf.plot(OHLC, type="candle", volume=True, addplot=mpf.make_addplot(EQUITY["open"]))
