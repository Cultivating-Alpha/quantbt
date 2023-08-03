from quantnb.lib import np, pd, time_manip
from quantnb.core.backtester import Backtester
from quantnb.core.enums import CommissionType, DataType
from quantnb.lib.output_trades import output_trades
import time

ohlc = pd.read_parquet("./data/EURUSD.parquet")
long = pd.read_parquet("./data/long_signals.parquet")
short = pd.read_parquet("./data/short_signals.parquet")


INITIAL_CAPITAL = 10000
# data = ohlc[0:15830]
data = ohlc[0:25830]
data = ohlc[0:100000]
# data = ohlc
data
data.reset_index(inplace=True)


def backtest(data, trades, initial_capital=INITIAL_CAPITAL):
    print("Compiling")
    bt = Backtester(
        commission=7,
        commission_type=CommissionType.FIXED,
        initial_capital=INITIAL_CAPITAL,
        slippage=0.0000,
        data_type=DataType.BID_ASK,
        date=time_manip.convert_datetime_to_ms(data["Date"]).values,
        bid=data["EURUSD.bid"].to_numpy(dtype=np.float32),
        ask=data["EURUSD.ask"].to_numpy(dtype=np.float32),
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

print("Preparing")
bt = backtest(data, long)

#
# len(bt.active_trades)
# #
# #
# # # stats = calculate_stats(data, bt)
# trades = output_trades(bt)
# print("======================================")
# trades

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

# |%%--%%| <pzU8rtj7OO|oEuBWcb7Ae>


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
