from quantnb.core.data_module import DataModule
from quantnb.core.enums import OrderDirection, Trade, OrderType, PositionCloseReason
from quantnb.core.data_module import DataModule
from quantnb.core.trade_module import TradeModule
from quantnb.core import print_bar
from quantnb.core.enums import DataType, Trade
from quantnb.core.specs_nb import backtester_specs
from numba.experimental import jitclass
import numpy as np

TRADE_ITEMS_COUNT = Trade.__len__()


# from quantnb.core.trade_module import DataModule


# pyright: reportGeneralTypeIssues=false
@jitclass(backtester_specs)
class FromSignals:
    data_module: DataModule.class_type.instance_type
    trade_module: TradeModule.class_type.instance_type

    def __init__(
        self,
        data_module: DataModule,
        trade_module: TradeModule,
    ) -> None:
        self.prev_percentage: int = 0
        self.data_module: DataModule = data_module
        self.trade_module: TradeModule = trade_module

    def was_trade_filled(self, i, date, last_trade, last_trade_index=None, debug=False):
        tick = date[i]
        next_tick = date[i + 1]

        if tick < last_trade <= next_tick:
            return True

        elif last_trade < tick:
            if debug:
                print("Skippped tick", last_trade_index, last_trade, tick, next_tick, i)
            return True
        else:
            return False

    def loop_updates(self, index):
        # UPDATE PNL OF TRADES
        self.trade_module.update_trades_pnl(self.data_module.close[index], 0, 0)

        # CLOSE TRADES
        self.trade_module.check_trades_to_close(
            self.data_module.get_data_at_index(index)
        )

        # UPDATE EQUITY
        self.data_module.update_equity(
            index, self.trade_module.closed_pnl, self.trade_module.floating_pnl
        )

    def from_signals(
        self,
        long_entries,
        long_exits,
        short_entries,
        short_exits,
        long_entry_price,
        short_entry_price,
        default_size=1,
    ):
        # print("Running")
        for i in range(len(long_entries)):
            if long_entries[i]:
                if default_size != 1:
                    entry_size = self.data_module.equity[i] / self.data_module.close[i]
                else:
                    entry_size = default_size
                self.trade_module.add_trade(
                    i,
                    OrderDirection.LONG.value,
                    OrderType.MARKET.value,
                    self.data_module.date[i],
                    long_entry_price[i],
                    entry_size,
                    0,
                    0,
                )
            elif long_exits[i]:
                # UPDATE PNL OF TRADES
                self.trade_module.update_trades_pnl(self.data_module.close[i], 0, 0)

                if len(self.trade_module.active_trades) == 0:
                    continue
                trade = self.trade_module.active_trades[-1]
                (
                    current_tick,
                    price_value,
                    bid,
                    ask,
                ) = self.data_module.get_data_at_index(i)

                price_data = (current_tick, short_entry_price[i], bid, ask)

                self.trade_module.close_trade(
                    trade, price_data, PositionCloseReason.SIGNAL.value
                )

            # if short_entries[i]:
            #     print("Need to go short")
            #     self.trade_module.add_trade(
            #         i,
            #         OrderDirection.SHORT.value,
            #         OrderType.MARKET.value,
            #         self.data_module.date[i],
            #         long_entry_price[i],
            #         1,
            #         0,
            #         0,
            #     )
            # elif short_exits[i]:
            #     # UPDATE PNL OF TRADES
            #     self.trade_module.update_trades_pnl(self.data_module.close[i], 0, 0)
            #
            #     if len(self.trade_module.active_trades) == 0:
            #         continue
            #     trade = self.trade_module.active_trades[-1]
            #     price_data = self.data_module.get_data_at_index(i)
            #
            #     self.trade_module.close_trade(
            #         trade, price_data, PositionCloseReason.SIGNAL.value
            #     )

            self.loop_updates(i)
        self.trade_module.reconcile()
