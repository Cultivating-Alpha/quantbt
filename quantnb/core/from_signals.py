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
        default_size=-1,
    ):
        # print("Running")
        max_active_trades = 0
        last_trade_index = 0
        for i in range(len(self.data_module.close)):
            can_trade = True
            if len(self.trade_module.active_trades) > 0:
                can_trade = False
            if long_entries[i] and can_trade:
                if default_size != 1:
                    entry_size = self.data_module.equity[i - 1] / self.data_module.close[i]  * default_size
                else:
                    entry_size = default_size
                # close__1 = self.data_module.close[i - 1]
                # open__1 = self.data_module.open[i - 1]
                # close = self.data_module.close[i]
                # open = self.data_module.open[i]
                # close_1 = self.data_module.close[i + 1]
                # open_1 = self.data_module.open[i + 1]
                # print("Close at i - 1: ", close__1)
                # print("Open at i - 1: ", open__1)
                # print()
                # print("Close at i: ", close)
                # print("Open at i: ", open)
                # print()
                # print("Close at i+1: ", close_1)
                # print("Open at i+1: ", open_1)
                #
                max_active_trades = max(
                    max_active_trades, len(self.trade_module.active_trades)
                )
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
                last_trade_index += 1
            elif long_exits[i]:
                # UPDATE PNL OF TRADES
                self.trade_module.update_trades_pnl(self.data_module.close[i], 0, 0)

                if len(self.trade_module.active_trades) != 0:
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

            self.loop_updates(i)
            if self.data_module.equity[i] < 0:
                # print("Account blown up")
                break
        # print(max_active_trades)
        self.trade_module.reconcile()
