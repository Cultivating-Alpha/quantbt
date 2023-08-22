from quantnb.core import FromTrades, FromSignals
from quantnb.core.enums import Trade, CommissionType, TradeSizeType
from quantnb.core.data_module import DataModule
from quantnb.core.trade_module import TradeModule
from quantnb.core.enums import DataType, Trade
from quantnb.lib.get_series_values import get_series_values
from quantnb.lib.shift_data import shift_data
import numpy as np


class Backtester:
    def __init__(
        self,
        date,
        close,
        open=None,
        high=None,
        low=None,
        bid=None,
        ask=None,
        data_type=DataType.BID_ASK,
        multiplier=1,
        commission=0.0,
        commission_type=CommissionType.FIXED,
        slippage=0.0,
        initial_capital=10000,
        default_trade_size=-1,
        trade_size_type=TradeSizeType.PERCENTAGE,
        max_active_trades=-1,
    ):
        if max_active_trades == -1:
            max_active_trades = 1000000

        self.trade_module = TradeModule(
            data_type=data_type.value,
            multiplier=multiplier,
            commission=commission,
            commission_type=commission_type.value,
            slippage=slippage,
            max_active_trades=max_active_trades,
        )
        self.data_module = DataModule(
            slippage=slippage,
            initial_capital=initial_capital,
            close=close,
            open=open,
            high=high,
            low=low,
            bid=bid,
            data_type=data_type,
            ask=ask,
            date=date,
            default_trade_size=default_trade_size,
            trade_size_type=trade_size_type.value,
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
        trailing_sl=None,
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
            get_series_values(trailing_sl),
        )
