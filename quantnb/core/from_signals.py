from quantnb.core.data_module import DataModule
from quantnb.core.enums import OrderDirection, Trade, OrderType, PositionCloseReason
from quantnb.core.data_module import DataModule
from quantnb.core.trade_module import TradeModule
from quantnb.core import print_bar
from quantnb.core.enums import DataType, Trade
from quantnb.core.specs_nb import backtester_specs
from numba.experimental import jitclass

TRADE_ITEMS_COUNT = Trade.__len__()


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
        # CLOSE TRADES
        self.trade_module.check_trades_to_close(
            self.data_module.get_data_at_index(index)
        )

        # UPDATE EQUITY
        self.data_module.update_equity(
            index, self.trade_module.closed_pnl, self.trade_module.floating_pnl
        )

    def close_trade(self, index, trade, exit_price):
        # Get the price data
        (
            current_tick,
            price_value,
            bid,
            ask,
        ) = self.data_module.get_data_at_index(index)
        price_data = (current_tick, exit_price, bid, ask)

        # Close the trade
        self.trade_module.close_trade(
            trade, price_data, PositionCloseReason.SIGNAL.value
        )

    def create_trade(self, direction, i, entry_price, sl=0.0, tp=0.0):
        entry_size = self.data_module.get_trade_size(i)
        self.trade_module.add_trade(
            i,
            direction,
            OrderType.MARKET.value,
            self.data_module.date[i],
            entry_price,
            entry_size,
            sl,
            tp,
        )

    def from_signals(
        self,
        long_entries,
        long_exits,
        short_entries,
        short_exits,
        long_entry_price,
        long_exit_price,
        short_entry_price,
        short_exit_price,
        sl,
        trailing_sl,
    ):
        last_trade_index = 0
        for i in range(len(self.data_module.close) - 1):
            # UPDATE PNL OF TRADES
            # TODO need to change how trade exit price is taken to be able to take next open for example
            self.trade_module.update_trades_pnl(self.data_module.open[i + 1], 0, 0)

            # Check if we are allowed to place more trades
            can_trade = True
            # if len(self.trade_module.active_trades) > 0:
            #     can_trade = False

            # ======================================================================================= #
            #                                          Take Long Trades                               #
            # ======================================================================================= #
            number_of_long_trades = self.trade_module.active_long_trades
            number_of_short_trades = self.trade_module.active_short_trades

            if trailing_sl[i] > 0:
                print(trailing_sl[i])

            if long_entries[i] and can_trade and number_of_long_trades == 0:
                self.create_trade(
                    OrderDirection.LONG.value, i, long_entry_price[i], sl[i]
                )
                last_trade_index += 1

            elif long_exits[i]:
                if len(self.trade_module.active_trades) != 0:
                    for trade in self.trade_module.active_trades:
                        if trade[Trade.Direction.value] == OrderDirection.LONG.value:
                            self.close_trade(i, trade, long_exit_price[i])

            # ======================================================================================= #
            #                                          Take Short Trades                               #
            # ======================================================================================= #
            if short_entries[i] and can_trade and number_of_short_trades == 0:
                self.create_trade(
                    OrderDirection.SHORT.value, i, short_entry_price[i], sl[i]
                )
                last_trade_index += 1

            elif short_exits[i]:
                if len(self.trade_module.active_trades) != 0:
                    for trade in self.trade_module.active_trades:
                        if trade[Trade.Direction.value] == OrderDirection.SHORT.value:
                            self.close_trade(i, trade, short_exit_price[i])

            self.loop_updates(i)

            if self.data_module.equity[i] < 0:
                print("Account blown up")
                break

        self.data_module.equity[-1] = self.data_module.equity[-2]
        self.trade_module.reconcile()
