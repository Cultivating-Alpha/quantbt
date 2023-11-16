import numpy as np
import pandas as pd
import seaborn as sns
import quantstats as qs
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
        use_trailing_sl=False,
        default_trade_size=-1.0,
        trade_size_type=TradeSizeType.PERCENTAGE,
        stop_to_be=None,
    ):
        self.commission = commission
        self.commission_type = commission_type
        self.multiplier = multiplier

        self.initial_capital = initial_capital
        self.use_sl = use_sl
        self.use_trailing_sl = use_trailing_sl
        self.slippage = slippage
        self.data_type = data_type
        self.params = ()
        self.default_trade_size = default_trade_size
        self.trade_size_type = trade_size_type
        self.stop_to_be = stop_to_be

        self.original_data = data[offset:]
        self.update_data(self.original_data.copy())

        self.set_backtester_settings()

    # ======================================================================================== #
    #                                     DATA Items
    # ======================================================================================== #
    def create_backtester(self):
        df = time_manip.format_index(self.data)
        open = df.open.to_numpy(dtype=np.float32)
        high = df.high.to_numpy(dtype=np.float32)
        low = df.low.to_numpy(dtype=np.float32)
        close = df.close.to_numpy(dtype=np.float32)

        self.bt = Backtester(
            initial_capital=self.initial_capital,
            commission=self.commission,
            commission_type=self.commission_type,
            multiplier=self.multiplier,
            open=open,
            high=high,
            low=low,
            close=close,
            data_type=self.data_type,
            date=time_manip.convert_datetime_to_ms(df["date"]).values,
            default_trade_size=self.default_trade_size,
            trade_size_type=self.trade_size_type,
            slippage=self.slippage,
        )

    def update_data(self, data):
        # data.rename(
        #     columns={"close": "Close", "high": "High", "low": "Low", "open": "Open"},
        #     inplace=True,
        # )
        data.index = data.index.astype(int) // 10**9
        self.data = data
        self.create_backtester()

    def data_days_ago(self, days=3):
        new_data = time_manip.hours_ago(self.original_data.copy(), 24 * days)
        self.update_data(new_data)

    def reset_data(self):
        self.update_data(self.original_data.copy())

    def set_data(self, data):
        self.update_data(data)

    # ======================================================================================== #
    #                                  BACKTESTING ITEMS                                       #
    # ======================================================================================== #
    def set_backtester_settings(
        self,
        one_trade_per_direction=True,
        trade_mode=TradeMode.HEDGE,
    ):
        self.one_trade_per_direction = one_trade_per_direction
        self.trade_mode = trade_mode
        self.trade_allowed = True

    def generate_signals(self, params=()):
        print("Stub function for generating signals")
        self.entries = np.full_like(self.data.close, False)
        self.exits = np.full_like(self.data.close, False)
        return {}

    def from_signals(self, params):
        self.bt.reset_backtester()
        self.params = params
        vals = self.generate_signals()

        default_values = {
            "long_exits": np.full_like(self.data.close, False),
            "short_exits": np.full_like(self.data.close, False),
            "sl": np.full_like(self.data.close, 0.0),
            "trailing_sl_long": np.full_like(self.data.close, 0.0),
            "trailing_sl_short": np.full_like(self.data.close, 0.0),
        }

        if not self.use_trailing_sl:
            vals["trailing_sl_long"] = default_values["trailing_sl_long"]
            vals["trailing_sl_short"] = default_values["trailing_sl_short"]

        for key in default_values.keys():
            if key not in vals:
                vals[key] = default_values[key]

        vals["trade_allowed"] = self.trade_allowed
        vals["stop_to_be"] = self.stop_to_be
        vals["one_trade_per_direction"] = self.one_trade_per_direction
        vals["trade_mode"] = self.trade_mode
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
        plotting.plot_equity(self.bt, self.data, "close")

    # ======================================================================================== #
    #                                         STATS
    # ======================================================================================== #
    def plot_monthly_returns(self):
        returns, equity_df = self.get_monthly_returns()

        data = returns.iloc[:, :-1]
        data = data[data != 0]

        # Create the heatmap with adjusted cell size and font size
        sns.heatmap(
            data,
            # cmap=GnRd,
            cmap="RdYlGn",
            annot=True,
            fmt=".1f",
            cbar=True,
            annot_kws={"size": 20},  # Adjust the font size for annotations
            linewidths=5,  # Add lines between cells for better separation
            square=True,  # Make cells square to ensure all values are visible
            vmin=-40,
            vmax=40,
        )

        plt.title("Monthly Values Heatmap")
        plt.xlabel("Month")
        plt.ylabel("Year")
        plt.show()
        print(returns)

        return returns, equity_df

    def get_monthly_returns(self):
        df = pd.DataFrame(
            {
                "equity": self.bt.data_module.equity,
            },
            index=time_manip.convert_ms_to_datetime(
                time_manip.convert_s_to_datetime(self.data.index.values)
            ),
        ).dropna()
        df["pct_change"] = df["equity"].pct_change()
        returns = qs.stats.monthly_returns(df["pct_change"])
        returns = np.round(returns * 100, 2)

        equity = df
        return returns, equity
