import numpy as np

from quantbt.core import FromSignals, FromTrades
from quantbt.core.data_module import DataModule
from quantbt.core.enums import CommissionType, DataType, Trade, TradeSizeType, TradeMode
from quantbt.core.trade_module import TradeModule
from quantbt.lib.get_series_values import get_series_values
from quantbt.lib.shift_data import shift_data


default_arguments = {
    "open": None,
    "high": None,
    "low": None,
    "bid": None,
    "ask": None,
    "data_type": DataType.BID_ASK,
    "multiplier": 1,
    "commission": 0.0,
    "commission_type": CommissionType.FIXED,
    "slippage": 0.0,
    "initial_capital": 10000,
    "default_trade_size": -1,
    "trade_size_type": TradeSizeType.PERCENTAGE,
    "max_active_trades": -1,
}


class Backtester:
    def __init__(self, date, close, **args):
        self.date = date
        self.close = close
        for arg in default_arguments.keys():
            if arg not in args.keys():
                setattr(self, arg, default_arguments[arg])
            else:
                setattr(self, arg, args[arg])
        self.reset_backtester()

    def reset_backtester(self):
        if self.max_active_trades == -1:
            self.max_active_trades = 1000000
        self.trade_module = TradeModule(
            data_type=self.data_type.value,
            multiplier=self.multiplier,
            commission=self.commission,
            commission_type=self.commission_type.value,
            slippage=self.slippage,
            max_active_trades=self.max_active_trades,
        )
        self.data_module = DataModule(
            slippage=self.slippage,
            initial_capital=self.initial_capital,
            close=self.close,
            open=self.open,
            high=self.high,
            low=self.low,
            bid=self.bid,
            data_type=self.data_type,
            ask=self.ask,
            date=self.date,
            default_trade_size=self.default_trade_size,
            trade_size_type=self.trade_size_type.value,
        )

    def from_trades(self, trades):
        # print("Compiling")
        self.bt = FromTrades(
            self.data_module,
            self.trade_module,
        )
        self.bt.from_trades(trades)

    def from_signals(
        self,
        short_entries=None,
        short_exits=None,
        long_entries=None,
        long_exits=None,
        long_entry_price=None,
        long_exit_price=None,
        short_entry_price=None,
        short_exit_price=None,
        sl=None,
        trailing_sl_long=None,
        trailing_sl_short=None,
        trade_allowed=True,
        stop_to_be=None,
        one_trade_per_direction=True,
        trade_mode=TradeMode.ONE_WAY,
    ):
        # print("Compiling")
        # print("Preparing")
        self.bt = FromSignals(
            self.data_module,
            self.trade_module,
        )

        # Calculate Entry and exit prices, if not provided by user
        shifted = shift_data(self.data_module.open, 1)
        if long_entry_price is None:
            long_entry_price = shifted
        if long_exit_price is None:
            long_exit_price = shifted
        if short_entry_price is None:
            short_entry_price = shifted
        if short_exit_price is None:
            short_exit_price = shifted

        # Run the backtest
        self.bt.from_signals(
            get_series_values(long_entries),
            get_series_values(long_exits),
            get_series_values(short_entries),
            get_series_values(short_exits),
            get_series_values(long_entry_price),
            get_series_values(long_exit_price),
            get_series_values(short_entry_price),
            get_series_values(short_exit_price),
            get_series_values(sl),
            get_series_values(trailing_sl_long),
            get_series_values(trailing_sl_short),
            trade_allowed,
            stop_to_be,
            one_trade_per_direction,
            trade_mode.value,
        )
