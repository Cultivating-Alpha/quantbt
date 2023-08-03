from typing import Optional, List
from quantnb.core.data_module import DataModule
from quantnb.core.enums import (
    OrderDirection,
    Trade,
)
from quantnb.core.data_module import DataModule
from quantnb.core.trade_module import TradeModule
from quantnb.core import print_bar, calculate_entry_price, create_new_trade
from quantnb.core.specs_nb import backtester_specs
from numba.experimental import jitclass

TRADE_ITEMS_COUNT = Trade.__len__()


# from quantnb.core.trade_module import DataModule


# pyright: reportGeneralTypeIssues=false
@jitclass(backtester_specs)
class Backtester:
    data_module: DataModule.class_type.instance_type
    trade_module: TradeModule.class_type.instance_type

    def __init__(
        self,
        data_module: DataModule,
        trade_module: TradeModule,
        commission=0.0,
        commission_type=2,
        slippage=0,
        slippage_type=1,
    ) -> None:
        self.prev_percentage: int = 0
        self.data_module: DataModule = data_module
        self.trade_module: TradeModule = trade_module

        # COMMISSIONS
        self.commission: float = commission
        self.commission_type: int = commission_type

        # SLIPPAGE
        self.slippage: int = slippage
        self.slippage_type: int = slippage_type

        # DATA
        print("Test without this")

    def was_trade_filled(self, i, ohlc, last_trade, last_trade_index=None, debug=False):
        tick = ohlc[i]
        next_tick = ohlc[i + 1]

        if tick < last_trade <= next_tick:
            return True

        elif last_trade < tick:
            if debug:
                print("Skippped tick", last_trade_index, last_trade, tick, next_tick, i)
            return True
        else:
            return False

    def update_equity(self, index):
        pnl = 0
        for trade in self.active_trades:
            pnl += trade[7]

        self.equity[index] = self.initial_capital + self.total_pnl + pnl

    def check_trades_to_close(self, current_tick, index):
        if len(self.active_trades) == 0:
            return
        has_new_trade = False
        for trade in self.active_trades:
            if trade[Trade.TIME_SL.value] < current_tick:
                # print("need to close trade")
                direction = trade[Trade.Direction.value]
                exit_price = calculate_exit_price(
                    self.slippage, direction, None, self.bid[index], self.ask[index]
                )

                new_trade = trade
                new_trade[Trade.Active.value] = False
                new_trade[Trade.ExitPrice.value] = exit_price
                new_trade[Trade.ExitTime.value] = current_tick
                new_trade[Trade.PNL.value] = PNL.calculate_trade_exit_pnl(trade)

                # Update Closed Trades
                self.closed_trades[self.last_closed_trade_index] = new_trade
                self.last_closed_trade_index += 1

                # Update total PNL
                self.total_pnl = PNL.calculate_realized_pnl(self.closed_trades)

                trade[Trade.Active.value] = False
                has_new_trade = True

        # Update Active Trades
        if has_new_trade:
            # self.active_trades[trade[Trade.Index.value]][Trade.Active.value] = False
            print("Have had a trade closed")
            # print(index)
            active_column = self.active_trades[:, Trade.Active.value]
            mask = active_column == True
            self.active_trades = self.active_trades[mask]
            # self.last_active_trade_index -= 1
        return

    def update_trades_pnl(self, index):
        self.active_trades = PNL.update_trades_pnl(
            self.active_trades,
            self.last_active_trade_index,
            commission=self.commission,
            commission_type=self.commission_type,
            data_type=self.data_type,
            price_value=self.close[index],
            bid=self.bid[index],
            ask=self.ask[index],
        )

    def add_trade(self, *args):
        # if self.debug:
        #     print("Adding new trade")
        if len(self.active_trades) >= 100:
            return
        self.last_active_trade_index += 1
        self.active_trades = create_new_trade(
            self.active_trades, self.last_active_trade_index, *args
        )

    def from_trades(self, trades, log_progress):
        last_trade_index = 0
        close = self.close
        print("==========")
        print(len(close))

        for i in range(len(close) - 1):
            self.prev_percentage = print_bar(i, len(close), self.prev_percentage)

            ### ==============================================================================  ####

            curr_trade = trades[last_trade_index]
            direction = (
                OrderDirection.LONG.value
                if curr_trade[3] == 1
                else OrderDirection.SHORT.value
            )
            volume = curr_trade[2]
            exit_time = curr_trade[1]

            if self.was_trade_filled(i, self.date, curr_trade[0], debug=False):
                price = calculate_entry_price(
                    self.slippage, direction, 0.0, self.bid[i], self.ask[i]
                )
                self.add_trade(
                    i, direction, curr_trade[0], price, volume, 0, 0, exit_time, 0
                )
                last_trade_index += 1

            # self.update_trades_pnl(i)
            # self.check_trades_to_close(self.date[i], i)
            # self.update_equity(i)

        print("done")
        self.closed_trades = self.closed_trades[: self.last_closed_trade_index]
        return 0
