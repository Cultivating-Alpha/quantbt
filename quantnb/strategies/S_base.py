import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from quantnb.lib.plotting import plotting
from quantnb.lib.time_manip import time_manip
from quantnb.core.backtester import Backtester
from quantnb.lib.output_trades import output_trades
from quantnb.lib.calculate_stats import calculate_stats
from quantnb.core.enums import DataType, CommissionType, TradeSizeType
<<<<<<< HEAD
=======

>>>>>>> master

class S_base:
    def __init__(
        self,
        data,
        offset=0,
        commission=0.0005,
        commission_type=CommissionType.PERCENTAGE,
        initial_capital=10000,
        data_type=DataType.OHLC,
        multiplier=1,
        default_size=None,
        use_sl=False,
        default_trade_size=-1.0,
        trade_size_type=TradeSizeType.PERCENTAGE,
    ):
        data = data[offset:]

        data.rename(
            columns={"close": "Close", "high": "High", "low": "Low", "open": "Open"},
            inplace=True,
        )
        data.index = data.index.astype(int) // 10**9
        self.data = data
        self.commmision = commission
        self.multiplier = multiplier
        self.default_size = default_size
        self.commmision_type = commission_type
        self.initial_capital = initial_capital
        self.use_sl = use_sl
        self.data_type = data_type
        self.params = ()
        self.default_trade_size= default_trade_size
        self.trade_size_type= trade_size_type

        self.set_bt_data()

    def set_bt_data(self):
        df = time_manip.format_index(self.data)
        open = df.Open.to_numpy(dtype=np.float32)
        high = df.High.to_numpy(dtype=np.float32)
        low = df.Low.to_numpy(dtype=np.float32)
        close = df.Close.to_numpy(dtype=np.float32)

        self.bt = Backtester(
            initial_capital=self.initial_capital,
            commission=self.commmision,
            commission_type=self.commmision_type,
            multiplier=self.multiplier,
            open=open,
            high=high,
            low=low,
            close=close,
            data_type=self.data_type,
            date=time_manip.convert_datetime_to_ms(df["Date"]).values,
            default_trade_size=self.default_trade_size,
            trade_size_type=self.trade_size_type,
        )

    # ======================================================================================== #
    #                                  BACKTESTING ITEMS                                       #
    # ======================================================================================== #
    def generate_signals(self, params=()):
        print("Stub function for generating signals")
        self.entries = np.full_like(self.data.Close, False)
        self.exits = np.full_like(self.data.Close, False)
        return {}

    def from_signals(self, params):
        self.params = params
        vals = self.generate_signals()
        if 'long_exits' not in vals:
            vals['long_exits'] = np.full_like(self.data.Close, False)
        if 'short_exits' not in vals:
            vals['short_exits'] = np.full_like(self.data.Close, False)
        if 'sl' not in vals:
            vals['sl'] = np.full_like(self.data.Close, 0.0)

        self.bt.from_signals(**vals)

    def from_trades(self, trades):
        self.bt.from_trades(trades)

    # ======================================================================================== #
    #                                 STATISTICS & METRICS                                     #
    # ======================================================================================== #
    def stats(self, display=False):
        params = self.params
        trades, closed_trades, active_trades = output_trades(self.bt)
        self.stats = calculate_stats(
            self.data,
            trades,
            closed_trades,
            self.bt.data_module.equity,
            self.initial_capital,
            display=display,
            index=[params],
        )
        return self.stats

    # Trades
    def trades(self):
        trades, closed_trades, active_trades = output_trades(self.bt)
        trades.sort_values(by=["EntryTime"], inplace=True)
        return trades

    def save_to_csv(self):
        print("Need to add CSV")

    # ======================================================================================== #
    #                                        Plotting                                          #
    # ======================================================================================== #
    def plot_equity(self):
        plotting.plot_equity(self.bt, self.data, "Close")
