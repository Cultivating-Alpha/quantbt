import numpy as np
import pandas as pd
from quantnb.core.backtester import Backtester
import matplotlib.pyplot as plt

from quantnb.helpers import save_to_csv, print_orders, print_trades, calculate_metrics


class S_base:
    def __init__(
        self, data, offset=0, commission=0.0002, initial_capital=10000, use_sl=False
    ):
        data = data[offset:]

        data.rename(
            columns={"close": "Close", "high": "High", "low": "Low", "open": "Open"},
            inplace=True,
        )
        data.index = data.index.astype(int) // 10**9
        self.data = data
        self.commmision = commission
        self.initial_capital = initial_capital
        self.use_sl = use_sl

        self.set_bt_data()

    def set_bt_data(self):
        df = self.data
        open = df.Open.to_numpy(dtype=np.float32)
        high = df.High.to_numpy(dtype=np.float32)
        low = df.Low.to_numpy(dtype=np.float32)
        close = df.Close.to_numpy(dtype=np.float32)
        index = df.index.to_numpy(dtype=np.int64)

        self.bt = Backtester(
            commissions=self.commmision, initial_capital=self.initial_capital
        )
        self.bt.set_data(open, high, low, close, index)

    def simulation(self, mode, use_sl):
        close = self.data.Close

        sl = None
        if self.use_sl:
            sl = self.sl.values

        size = np.full_like(close, 1)
        multiplier = 1
        size = size * multiplier

        self.bt.from_signals(self.entries, self.exits, sl, use_sl)

        return (
            self.bt.final_value,
            self.bt.equity,
            self.bt.orders[: self.bt.order_idx, :],
            self.bt.trades[: self.bt.trade_idx, :],
        )

    def backtest_bid_ask(self, params):
        pass

    def backtest(self, params):
        self.get_signals(params)
        (final_value, equity, orders_arr, trades_arr) = self.simulation(
            mode=1, use_sl=self.use_sl
        )
        self.orders_arr = orders_arr

        dd, total_return, ratio, buy_and_hold = calculate_metrics(
            equity, self.data, final_value, self.initial_capital
        )

        self.stats = pd.DataFrame(
            {
                "final_value": final_value,
                "dd": dd,
                "total_return": total_return,
                "ratio": ratio,
                "buy_and_hold": buy_and_hold,
            },
            index=[0],
        )

        self.trades_arr = trades_arr
        self.equity = equity
        # print(self.stats)

    # HELPERS
    def print_trades(self):
        print_trades(self.trades_arr)

    def save_to_csv(self):
        data = self.data.copy()
        data.reset_index(inplace=True)
        data.rename(columns={"timestamp": "Date"}, inplace=True)
        data.set_index("Date", inplace=True)

        save_to_csv(
            data,
            self.ma_long,
            self.ma_short,
            self.rsi,
            self.atr,
            self.entries,
            self.orders_arr,
            self.equity,
            "",
        )

    def plot_equity(self):
        returns = pd.Series(self.equity, index=self.data.index)
        returns.plot()
        plt.show()
