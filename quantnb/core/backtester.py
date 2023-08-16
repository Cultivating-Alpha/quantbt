from quantnb.core import FromTrades, FromSignals
from quantnb.core.enums import Trade, CommissionType
from quantnb.core.data_module import DataModule
from quantnb.core.trade_module import TradeModule
from quantnb.core.enums import DataType, Trade
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
        commission=0,
        commission_type=CommissionType.FIXED,
        slippage=0,
        initial_capital=10000,
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
        )

    def from_trades(self, trades):
        # print("Compiling")
        self.bt = FromTrades(
            self.data_module,
            self.trade_module,
        )
        return self.bt.from_trades(trades)

    def from_signals(
        self,
        short_entries=None,
        short_exits=None,
        long_entries=None,
        long_exits=None,
        long_entry_price=None,
        short_entry_price=None,
        default_size=-1,
    ):
        # print("Compiling")
        # print("Preparing")
        self.bt = FromSignals(
            self.data_module,
            self.trade_module,
        )

        self.bt.from_signals(
            long_entries,
            long_exits,
            short_entries,
            short_exits,
            # long_entry_price.to_numpy(dtype=np.float32),
            # short_entry_price.to_numpy(dtype=np.float32),
            long_entry_price,
            short_entry_price,
            default_size
        )
