import numba as nb
import numpy as np
from numba import float32, int32

from typing import List

from enum import Enum, IntEnum


class OrderType(IntEnum):
    LONG = 1
    SHORT = 2


@nb.experimental.jitclass()
class Backtester:
    # DATA
    open: float32[:]
    high: float32[:]
    low: float32[:]
    close: float32[:]
    date: int32[:]

    # PORTFOLIO
    cash: int32
    final_value: float32
    total_pnl: float32
    equity: float32[:]

    # TRADE MANAGEMENT
    in_position: nb.boolean
    stop_loss: float32
    entry_time: int32
    entry_size: float32
    entry_price: float32
    commissions: float32

    # MISC
    order_idx: int32
    trade_idx: int32
    orders: float32[:, :]
    trades: float32[:, :]

    def __init__(self, initial_capital=10000, commissions=0.0):
        # PORTFOLIO
        self.cash = initial_capital
        self.final_value = initial_capital
        self.total_pnl = 0.0

        # TRADE MANAGEMENT
        self.in_position = False
        self.stop_loss = 0
        self.entry_time = 0
        self.entry_size = 0
        self.entry_price = 0
        self.commissions = commissions

        # MISC
        self.order_idx = 0
        self.trade_idx = 0

    def set_data( self, open, high, low, close, date):
        # DATA
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.date = date

        # PORTFOLIO
        self.equity = np.empty(len(self.close), dtype=float32)
        self.equity[0] = self.cash

        # MISC
        self.orders = np.zeros((len(self.close), 5), dtype=float32)
        self.trades = np.zeros((len(self.close), 6), dtype=float32)

    @staticmethod
    def calculate_fees(price, size, commissions):
        return price * size * commissions

    def new_order(self, i, order_type, close):
        self.orders[self.order_idx, :] = [
            i,
            order_type.value,
            close,
            self.entry_size,
            self.cash,
        ]
        self.order_idx += 1

    def go_long(self, i):
        close = self.close[i]

        self.entry_size = self.cash / self.close[i]

        fee = self.calculate_fees(close, self.entry_size, self.commissions)
        self.cash -= self.entry_size * close - fee

        self.new_order(i, OrderType.LONG, close)

        self.entry_time = self.date[i]
        # print(f"Entry time: {self.entry_time}")
        self.entry_price = close
        self.in_position = True

    def close_position(self, i, exit_price):
        close = self.close[i]

        fee = self.calculate_fees(close, self.entry_size, self.commissions)
        self.cash = self.entry_size * exit_price - fee

        self.new_order(i, OrderType.SHORT, close)

        pnl = (exit_price - self.entry_price) * self.entry_size - fee
        self.total_pnl += pnl

        self.trades[self.trade_idx, :] = [
            self.entry_time,
            self.date[i],
            self.entry_price,
            exit_price,
            pnl,
            self.entry_size,
        ]
        self.trade_idx += 1
        self.entry_size = 0
        self.in_position = False

    def backtest(self, entry_signals, exit_signals, sl, use_sl=True, mode=1, debug=False):
        close = self.close
        stop_loss = 0

        if debug:
            print("Backtest launched")

        for i in range(1, len(close)):
            if debug:
                print(f"========== {i}")
            if entry_signals[i]:
                if not self.in_position:
                    stop_loss = sl[i]
                    self.go_long(i)

            elif exit_signals[i]:
                if self.in_position:
                    self.close_position(i, close[i])

            if use_sl and self.in_position:
                if mode == 1:
                    if close[i] < stop_loss:
                        self.close_position(i, self.open[i + 1])
                elif mode == 2:
                    if self.low[i] < stop_loss:
                        self.close_position(i, stop_loss)

            fee = self.calculate_fees(close[i], self.entry_size, self.commissions)
            self.equity[i] = self.cash + self.entry_size * close[i] - fee

        self.final_value = self.equity[-1]


# import pandas as pd
# from numba.typed import List as NumbaList
#
# data = pd.read_parquet("./data/uniswap-v3-WETH-USDC-h4.parquet")
# data.index = data.index.astype(int) // 10**9
# # data = data[0:400]
# # data
#
# # bt.orders
#
#
# def simulation(data, entries, exits, sl, mode, use_sl):
#     close = data.close
#     size = np.full_like(close, 1)
#     multiplier = 1
#     size = size * multiplier
#     # fees = np.full_like(prices, 2.2)
#     bt = Backtester(
#         NumbaList(data.open),
#         NumbaList(data.high),
#         NumbaList(data.low),
#         NumbaList(data.close),
#         NumbaList(data.index),
#         commissions=0.0005,
#     )
#     bt.backtest(entries.values, exits.values, sl.values)
#
#     return (
#         bt.final_value,
#         bt.equity,
#         bt.orders[: bt.order_idx, :],
#         bt.trades[: bt.trade_idx, :],
#     )
#
#
# from temp import SMA, print_trades, plot_equity, calculate_metrics
# import talib
#
#
# def get_signals(data, long, short, cutoff=5, atr_distance=2):
#     close = data.close
#     ma_long = SMA(close, long)
#     ma_short = SMA(close, short)
#     rsi = talib.RSI(close, timeperiod=2)
#     atr = talib.ATR(data.high, data.low, close, 14)
#
#     # entry_signals = ma_long.vbt.crossed_below(ma_short)
#     # exit_signals = ma_long.vbt.crossed_above(ma_short)
#     # entries = np.logical_and(close >= ma_long, rsi <= cutoff)
#     entries = np.logical_and(
#         close <= ma_short, np.logical_and(close >= ma_long, rsi <= cutoff)
#     )
#     exits = close > ma_short
#     # exits = rsi > 70
#
#     sl = data.low - atr * atr_distance
#     return entries, exits, ma_long, ma_short, rsi, atr, sl
#
#
# # entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(data, 200, 11, 9, 2.5)
#
# # |%%--%%| <nzZ8LJSl7P|8TjcgBdqvP>
# entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(data, 295, 11, 9, 2.5)
# # entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(data, 216, 9, 13, 2)
# # entries, exits, ma_long, ma_short, rsi, atr, sl = get_signals(data, 216, 50, 20, 2)
# (final_value, equity, orders_arr, trades_arr) = simulation(
#     data, entries, exits, sl, mode=1, use_sl=True
# )
# print_trades(trades_arr)
#
# dd, total_return, ratio = calculate_metrics(equity, data, final_value)
#
# newdf = pd.DataFrame(
#     {
#         "final_value": final_value,
#         "dd": dd,
#         "total_return": total_return,
#         "ratio": ratio,
#     },
#     index=[0],
# )
#
# print(newdf)
