from quantnb.core.data_module import DataModule
from quantnb.core.enums import OrderDirection, Trade, OrderType
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
class FromTrades:
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

    def from_trades(self, trades):
        last_trade_index = 0
        close = self.data_module.close
        print("========== FROM TRADES")
        max_active_trades = 0
        last_index = 0
        print(trades)

        for i in range(len(close)):
            self.prev_percentage = print_bar(i, len(close), self.prev_percentage)
            if last_trade_index >= len(trades):
                break

            # ### ==============================================================================  ####
            no_more_trades = False
            while not no_more_trades and last_trade_index < len(trades):
                curr_trade = trades[last_trade_index]
                direction = (
                    OrderDirection.LONG.value
                    if curr_trade[3] == 1
                    else OrderDirection.SHORT.value
                )
                exit_time = curr_trade[1] if curr_trade[1] != -1 else np.inf
                volume = curr_trade[2]

                if self.was_trade_filled(
                    i, self.data_module.date, curr_trade[0], debug=False
                ):
                    entry_price = self.data_module.calculate_entry_price(i, direction)

                    self.trade_module.add_trade(
                        i,
                        direction,
                        OrderType.MARKET.value,
                        self.data_module.date[i],
                        entry_price,
                        volume,
                        0,
                        0,
                        exit_time,
                        curr_trade[4],  # extra
                    )
                    last_trade_index += 1
                else:
                    no_more_trades = True

            # Update PNL | Check trades to close | Update Equity
            self.loop_updates(i)
            max_active_trades = max(max_active_trades, len(self.trade_module.active_trades))
            last_index = i

        print(max_active_trades)
        self.trade_module.reconcile()
        self.data_module.equity = self.data_module.equity[: last_index + 1]
        return 0
