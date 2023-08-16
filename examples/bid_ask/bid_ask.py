from quantnb.lib import np, pd, time_manip
from quantnb.core.backtester import Backtester
from quantnb.core.data_module import DataModule
from quantnb.core.trade_module import TradeModule
from quantnb.core.enums import CommissionType, DataType, Trade
from quantnb.lib.output_trades import output_trades
from quantnb.lib.calculate_stats import calculate_stats
from quantnb.lib.plotting import plotting
import time

ohlc = pd.read_parquet("./data/EURUSD.parquet")



# long = pd.read_parquet("./data/long_signals.parquet")
# short = pd.read_parquet("./data/short_signals.parquet")
signals = pd.read_parquet("./data/trades.parquet")

INITIAL_CAPITAL = 10000
SLIPPAGE = 0
MAX_ACTIVE_TRADES = 100000
COMMISSION = 0
# data = ohlc[0:15830]
# data = ohlc[0:25830]
data = ohlc[0:1000000]
# data = ohlc[0:57000]
# data = ohlc
data.reset_index(inplace=True)
data




def strip_signals(data, signals):
    converted = time_manip.convert_datetime_to_ms(data['Date'])
    start = converted[0]
    end = converted[len(converted) - 1]
    signals = signals[signals['entry'] >= start]
    signals = signals[signals['entry'] <= end]
    return signals


signals = strip_signals(data, signals)


display = signals.copy()
display['entry'] = time_manip.convert_ms_to_datetime(display['entry'])
display
#|%%--%%| <OtQtL9beIy|B3OnFOAtZc>


# bt.trade_module

def backtest(data, trades, initial_capital=INITIAL_CAPITAL):
    bt = Backtester(
        close=data["EURUSD.bid"].to_numpy(dtype=np.float32),
        data_type=DataType.BID_ASK,
        bid=data["EURUSD.bid"].to_numpy(dtype=np.float32),
        ask=data["EURUSD.ask"].to_numpy(dtype=np.float32),
        date=time_manip.convert_datetime_to_ms(data["Date"]).values,
        max_active_trades=MAX_ACTIVE_TRADES,
    )
    bt.from_trades(trades.values)

    return bt


bt = backtest(data, signals)


output_trades(bt)[0]
bt.trade_module.closed_pnl


df = pd.DataFrame(bt.data_module.equity)
df.plot()
plt.show()

df.tail(10)

# |%%--%%| <B3OnFOAtZc|TpMPbSwUoE>

equity = bt.data_module.equity

plotting.plot_equity(equity, data, "EURUSD.bid")
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

# |%%--%%| <TpMPbSwUoE|oEuBWcb7Ae>


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
