from cycler import mul
import numpy as np
from quantnb.core.enums import OrderType
import numpy as np
import numba as nb
from numba import float32, int32, int64
from numba import from_dtype, njit

from typing import List

dt = np.dtype([("x", np.float32), ("y", np.float32)])
nb_dt = from_dtype(dt)


@nb.experimental.jitclass
class Base:
    def __init__(
        self,
        initial_capital=10000,
        commission=0.0,
        commission_type="percentage",
        multiplier=1,
        default_size=None,
        slippage=None,
        slippage_type="fixed",
    ):
        # PORTFOLIO
        self.cash = initial_capital
        self.initial_capital = initial_capital
        self.final_value = initial_capital
        self.total_pnl = 0.0
        self.multiplier = multiplier
        if default_size is not None:
            self.default_size = default_size
        else:
            self.default_size = -1

        if slippage is not None:
            self.slippage = slippage
        self.slippage_type = slippage_type

        # TRADE MANAGEMENT
        self.in_position = False
        self.stop_loss = 0
        self.entry_time = 0
        self.entry_size = 0
        self.entry_price = 0
        self.commission = commission
        self.commission_type = commission_type

        # MISC
        self.order_idx = 0
        self.trade_idx = 0

        # POSITION MANAGEMENT
        self.total_volume = 0
        self.weighted_sum = 0

    def set_bid_ask_data(self, date, bid, ask, volume=None):
        # DATA
        self.date = date
        self.bid = bid
        self.ask = ask
        self.close = bid
        if volume is not None:
            self.volume = volume

        self.set_general()

    def set_data(self, open, high, low, close, date):
        # DATA
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.date = date

        self.set_general()

    def set_general(self):
        # PORTFOLIO
        self.equity = np.empty(len(self.close), dtype=float32)
        self.equity[0] = self.cash

        # MISC
        self.orders = np.zeros((len(self.close), 5), dtype=float32)
        self.trades = np.zeros((len(self.close), 10), dtype=float32)
