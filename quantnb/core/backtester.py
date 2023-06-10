import numba as nb
import numpy as np
from numba import float32, int32
from quantnb.core.enums import OrderType

from typing import List


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
    current_trade_type: int32

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

    def set_data(self, open, high, low, close, date):
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
        self.trades = np.zeros((len(self.close), 7), dtype=float32)

    # ===================================================================================== #
    #                                       HELPERS                                         #
    # ===================================================================================== #

    @staticmethod
    def calculate_fees(price, size, commissions):
        return price * size * commissions

    # ===================================================================================== #

    #                                POSITION MANAGEMENT                                    #
    # ===================================================================================== #
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

        self.current_trade_type = OrderType.LONG.value

    def go_short(self, i):
        close = self.close[i]

        self.entry_size = self.cash / self.close[i]

        fee = self.calculate_fees(close, self.entry_size, self.commissions)
        self.cash -= self.entry_size * close - fee

        self.new_order(i, OrderType.SHORT, close)

        self.entry_time = self.date[i]
        # print(f"Entry time: {self.entry_time}")
        self.entry_price = close
        self.in_position = True

        self.current_trade_type = OrderType.LONG.value

    def close_position(self, i, exit_price):
        close = self.close[i]

        fee = self.calculate_fees(close, self.entry_size, self.commissions)
        self.cash = self.entry_size * exit_price - fee

        order_type = OrderType.LONG
        if self.current_trade_type == OrderType.LONG.value:
            order_type = OrderType.SHORT
        self.new_order(i, order_type, close)

        pnl = (exit_price - self.entry_price) * self.entry_size - fee
        self.total_pnl += pnl

        self.trades[self.trade_idx, :] = [
            self.entry_time,
            self.date[i],
            self.entry_price,
            exit_price,
            pnl,
            self.entry_size,
            self.current_trade_type,
        ]
        self.trade_idx += 1
        self.entry_size = 0
        self.in_position = False

    # ===================================================================================== #
    #                                       CORE BACKTESTER                                 #
    # ===================================================================================== #

    def backtest(
        self, entry_signals, exit_signals, sl=None, use_sl=False, mode=1, debug=False
    ):
        close = self.close
        stop_loss = 0

        if debug:
            print("Backtest launched")

        for i in range(1, len(close)):
            if debug:
                print(f"========== {i}")
            if entry_signals[i]:
                if not self.in_position:
                    if use_sl and sl is not None:
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
