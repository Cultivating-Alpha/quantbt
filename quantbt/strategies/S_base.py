import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from quantbt.lib.plotting import plotting
from quantbt.lib.time_manip import time_manip
from quantbt.core.backtester import Backtester
from quantbt.lib.output_trades import output_trades
from quantbt.lib.calculate_stats import calculate_stats
from quantbt.core.enums import DataType, CommissionType, TradeSizeType, TradeMode


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
        slippage=0.0,
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
        self.initial_capital = initial_capital
        self.use_sl = use_sl
        self.slippage = slippage
        self.data_type = data_type
        self.params = ()
        self.default_trade_size = default_trade_size
        self.trade_size_type = trade_size_type

        df = time_manip.format_index(self.data)
        open = df.Open.to_numpy(dtype=np.float32)
        high = df.High.to_numpy(dtype=np.float32)
        low = df.Low.to_numpy(dtype=np.float32)
        close = df.Close.to_numpy(dtype=np.float32)

        self.bt = Backtester(
            initial_capital=initial_capital,
            commission=commission,
            commission_type=commission_type,
            multiplier=multiplier,
            open=open,
            high=high,
            low=low,
            close=close,
            data_type=data_type,
            date=time_manip.convert_datetime_to_ms(df["Date"]).values,
            default_trade_size=default_trade_size,
            trade_size_type=trade_size_type,
            slippage=self.slippage,
        )

    # ======================================================================================== #
    #                                  BACKTESTING ITEMS                                       #
    # ======================================================================================== #
    def generate_signals(self, params=()):
        print("Stub function for generating signals")
        self.entries = np.full_like(self.data.Close, False)
        self.exits = np.full_like(self.data.Close, False)
        return {}

    def from_signals(
        self,
        params,
        use_trailing_sl=True,
        trade_allowed=True,
        stop_to_be=None,
        one_trade_per_direction=True,
        trade_mode=TradeMode.ONE_WAY,
    ):
        self.bt.reset_backtester()
        self.params = params
        vals = self.generate_signals()

        default_values = {
            "long_exits": np.full_like(self.data.Close, False),
            "short_exits": np.full_like(self.data.Close, False),
            "sl": np.full_like(self.data.Close, 0.0),
            "trailing_sl_long": np.full_like(self.data.Close, 0.0),
            "trailing_sl_short": np.full_like(self.data.Close, 0.0),
        }

        if not use_trailing_sl:
            vals["trailing_sl_long"] = default_values["trailing_sl_long"]
            vals["trailing_sl_short"] = default_values["trailing_sl_short"]

        for key in default_values.keys():
            if key not in vals:
                vals[key] = default_values[key]

        vals["trade_allowed"] = trade_allowed
        vals["stop_to_be"] = stop_to_be
        vals["one_trade_per_direction"] = one_trade_per_direction
        vals["trade_mode"] = trade_mode
        self.bt.from_signals(**vals)

    def from_trades(self, trades):
        self.bt.from_trades(trades)

    # ======================================================================================== #
    #                                 STATISTICS & METRICS                                     #
    # ======================================================================================== #
    def get_stats(self, display=False):
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
    def get_trades(self, columns_to_drop=[], close_active_trades=False):
        trades, closed_trades, active_trades = output_trades(
            self.bt, close_active_trades=close_active_trades
        )
        trades.sort_values(by=["EntryTime"], inplace=True)

        trades.drop(columns=columns_to_drop, inplace=True, axis=1)
        return trades

    # ======================================================================================== #
    #                                        Plotting                                          #
    # ======================================================================================== #
    def plot_equity(self):
        plotting.plot_equity(self.bt, self.data, "Close")
