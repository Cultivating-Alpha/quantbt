from quantnb.lib import np, pd, time_manip
from quantnb.core.backtester import Backtester
from quantnb.core.data_module import DataModule
from quantnb.core.trade_module import TradeModule
from quantnb.core.enums import CommissionType, DataType, Trade
from quantnb.lib.output_trades import output_trades
import time

ohlc = pd.read_parquet("./data/EURUSD.parquet")
long = pd.read_parquet("./data/long_signals.parquet")
short = pd.read_parquet("./data/short_signals.parquet")


INITIAL_CAPITAL = 10000
SLIPPAGE = 0
MAX_ACTIVE_TRADES = 10
COMMISSION = 0
# data = ohlc[0:15830]
data = ohlc[0:25830]
data = ohlc[0:50000]
data = ohlc[0:1000000]
data = ohlc
data
data.reset_index(inplace=True)


def backtest(data, trades, initial_capital=INITIAL_CAPITAL):
    bt = Backtester(
        close=data["EURUSD.bid"].to_numpy(dtype=np.float32),
        data_type=DataType.BID_ASK,
        bid=data["EURUSD.bid"].to_numpy(dtype=np.float32),
        ask=data["EURUSD.ask"].to_numpy(dtype=np.float32),
        date=time_manip.convert_datetime_to_ms(data["Date"]).values,
        max_active_trades=1,
    )
    print("running trade function")
    start = time.time()
    bt.from_trades(trades.values)
    end = time.time()
    print("Time taken: ", end - start)

    return bt


data.tail()
time_manip.convert_ms_to_datetime(long["long_entry"]).head(10)
time_manip.convert_ms_to_datetime(long["long_exit"]).head(15)
long.columns
long
bt = backtest(data, long)
#
closed = bt.trade_module.closed_trades
active = bt.trade_module.active_trades
print(len(closed))
print(len(active))
# # len(bt.active_trades)
print(len(closed + len(active)))
# #
# #
# # #
# # # #
# # # # # stats = calculate_stats(data, bt)
# # print(bt.trade_module.closed_trades)
# # print(bt.trade_module.active_trades)
# pnl = bt.trade_module.closed_trades[0][Trade.PNL.value]
# pnl
#
# trades = output_trades(bt)
# # # print("======================================")
# # trades["PNL"]
# trades
# trades["Direction"]
# trades["EntryPrice"]
# print(bt.data_module.close[-1])

# trades.to_parquet("./quantnb/tests/sample_trades.parquet")

# # trades[:-1]
# #
# # # trades[:-1]["PNL"].sum()
# trades
# print(trades["PNL"].sum())
# # num = trades["PNL"].sum()
# # num
# # 10000 - 378
# # trades
# # # #
# # # trades
# # # bt.closed_trades
# # bt.active_trades
# # bt.trades
# #
# # trades
# # data

# |%%--%%| <qZJhfDnqmc|oEuBWcb7Ae>


from numba import njit


@njit
def test():
    for i in range(0, 25964964):
        a = i * 4


start = time.time()
test()
end = time.time()
print("Time taken: ", end - start)


@njit
def from_trades(close):
    for i in range(len(close) - 1):
        a = i * 4
        # self.prev_percentage = print_bar(i, len(close), self.prev_percentage)

        ### ==============================================================================  ####

        # curr_trade = trades[last_trade_index]
        # direction = (
        #     OrderDirection.LONG.value
        #     if curr_trade[3] == 1
        #     else OrderDirection.SHORT.value
        # )
        # volume = curr_trade[2]
        # exit_time = curr_trade[1]
        #
        # if self.was_trade_filled(i, self.date, curr_trade[0], debug=False):
        #     price = calculate_trade_price(
        #         self.slippage, direction, None, self.bid[i], self.ask[i]
        #     )
        #     self.add_trade(
        #         i, direction, curr_trade[0], price, volume, 0, 0, exit_time, 0
        #     )
        #     last_trade_index += 1

        # self.update_trades_pnl(i)
        # self.check_trades_to_close(self.date[i], i)
        # self.update_equity(i)

    print("done")
    return 0


start = time.time()
from_trades(ohlc["EURUSD.bid"].values)
end = time.time()
print("Time taken: ", end - start)

# |%%--%%| <oEuBWcb7Ae|RMN0xBziF2>

from typing import List
from numba.experimental import jitclass
from numba.typed import List as NumbaList


@jitclass
class Counter:
    value: int

    def __init__(self):
        self.value = 0

    def get(self) -> int:
        ret = self.value
        self.value += 1
        return ret


@jitclass
class ListLoopIterator:
    counter: Counter
    items: List[float]

    def __init__(self, items: List[float]):
        self.items = items
        self.counter = Counter()

    def get(self) -> float:
        idx = self.counter.get() % len(self.items)
        return self.items[idx]


items = NumbaList([3.14, 2.718, 0.123, -4.0])
loop_itr = ListLoopIterator(items)
