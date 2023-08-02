import numpy as np
from quantnb.core.enums import (
    OrderDirection,
    CommissionType,
    SlippageType,
    Trade,
    DataType,
)
import numpy as np
import quantnb.core.PNL as PNL
from quantnb.core import (
    spec,
    print_bar,
    calculate_commission,
    calculate_trade_price,
    calculate_exit_price,
    create_new_trade,
)

TRADE_ITEMS_COUNT = Trade.__len__()


# @nb.experimental.jitclass(spec)
class Backtester:
    def __init__(
        self,
        initial_capital=10000,
        multiplier=1,  # leverage multiplier
        commission=0.0,
        commission_type=2,
        size=-1,
        size_type=1,
        slippage=0,
        slippage_type=1,
        data_type=0,
        open=None,
        high=None,
        low=None,
        close=None,
        bid=None,
        ask=None,
        date=None,
    ):
        # PORTFOLIO
        self.initial_capital = initial_capital
        self.final_value = initial_capital
        self.total_pnl = 0.0
        self.multiplier = multiplier
        self.last_active_trade_index = 0
        self.last_closed_trade_index = 0
        self.data_type = data_type

        # MISC

        # SIZE
        self.size = size
        self.size_type = size_type

        # COMMISSIONS
        self.commission = commission
        self.commission_type = commission_type

        # SLIPPAGE
        self.slippage = slippage
        self.slippage_type = slippage_type

        # DATA
        self.date = date
        if data_type == DataType.OHLC.value:
            if open is not None:
                self.open = open
                self.high = high
                self.low = low
                self.close = close
        else:
            if bid is not None:
                self.bid = bid
                self.ask = ask
            self.close = self.bid

        # PORTFOLIO
        self.equity = np.empty(len(self.close), dtype=np.float32)
        self.equity[0] = self.initial_capital

        # MISC
        self.active_trades = np.zeros(
            (len(self.close), TRADE_ITEMS_COUNT), dtype=np.float32
        )
        self.closed_trades = np.zeros(
            (len(self.close), TRADE_ITEMS_COUNT), dtype=np.float32
        )
        self.prev_percentage = 0

    # # ===================================================================================== #
    # #                                POSITION MANAGEMENT                                    #
    # # ===================================================================================== #
    # def new_order(self, i, order_type, close):
    #     self.orders[self.order_idx, :] = [
    #         i,
    #         order_type.value,
    #         close,
    #         self.entry_size,
    #         self.cash,
    #     ]
    #     self.order_idx += 1
    #
    # def go_long(self, price, i):
    #     # self.entry_size = self.cash / self.close[i]
    #
    #     fee = calculate_fees(
    #         price, self.entry_size, self.commission, self.commission_type
    #     )
    #     self.cash -= self.entry_size * price - fee
    #
    #     self.new_order(i, OrderType.LONG, price)
    #
    #     self.entry_time = self.date[i]
    #     # print(f"Entry time: {self.entry_time}")
    #     self.entry_price = price
    #     self.in_position = True
    #
    #     self.current_trade_type = OrderType.LONG.value
    #
    # def go_short(self, i):
    #     close = self.close[i]
    #
    #     fee = self.calculate_fees(
    #         close, self.entry_size, self.commission, self.commission_type
    #     )
    #     self.cash -= self.entry_size * close - fee
    #
    #     self.new_order(i, OrderType.SHORT, close)
    #
    #     self.entry_time = self.date[i]
    #     # print(f"Entry time: {self.entry_time}")
    #     self.entry_price = close
    #     self.in_position = True
    #
    #     self.current_trade_type = OrderType.LONG.value
    #
    # def close_position(self, i, exit_price):
    #     close = self.close[i]
    #
    #     fee = self.calculate_fees(
    #         close, self.entry_size, self.commission, self.commission_type
    #     )
    #     # print("closing position")
    #     # print(self.cash)
    #     # print(self.cash)
    #
    #     order_type = OrderType.LONG
    #     if self.current_trade_type == OrderType.LONG.value:
    #         order_type = OrderType.SHORT
    #     self.new_order(i, order_type, close)
    #
    #     if self.commission_type == "percentage":
    #         # print("need to update commissions calculation of percentage trades")
    #         entry_fee = self.entry_price * self.entry_size * self.commission
    #     elif self.commission_type == "fixed":
    #         fee = fee * 2
    #
    #     pnl = (exit_price - self.entry_price) * self.entry_size * self.multiplier - fee
    #     self.cash += self.entry_size * exit_price - fee
    #     self.total_pnl += pnl
    #
    #     self.trades[self.trade_idx, :] = [
    #         self.trade_idx,
    #         self.current_trade_type,
    #         self.entry_time,
    #         self.entry_price,
    #         self.date[i],
    #         exit_price,
    #         self.entry_size,
    #         pnl,
    #         fee,
    #         False,
    #     ]
    #
    #     self.trade_idx += 1
    #     self.entry_size = 0
    #     self.in_position = False
    #
    # # ===================================================================================== #
    # #                                       CORE BACKTESTER                                 #
    # # ===================================================================================== #
    # def from_signals(
    #     self, entry_signals, exit_signals, sl=None, use_sl=False, mode=1, debug=False
    # ):
    #     close = self.close
    #     stop_loss = 0
    #
    #     if debug:
    #         print("Backtest launched")
    #
    #     for i in range(1, len(close)):
    #         if debug:
    #             print(f"========== {i}")
    #         if entry_signals[i]:
    #             if not self.in_position:
    #                 # print("GOING LONG")
    #                 if use_sl and sl is not None:
    #                     stop_loss = sl[i]
    #
    #                 self.entry_size = self.cash / self.close[i]
    #                 if self.default_size > 0:
    #                     self.entry_size = self.default_size
    #                 self.go_long(self.close[i], i)
    #
    #         elif exit_signals[i]:
    #             if self.in_position:
    #                 self.close_position(i, close[i])
    #
    #         if use_sl and self.in_position:
    #             if mode == 1:
    #                 if close[i] < stop_loss:
    #                     self.close_position(i, self.open[i + 1])
    #             elif mode == 2:
    #                 if self.low[i] < stop_loss:
    #                     self.close_position(i, stop_loss)
    #
    #         fee = self.calculate_fees(
    #             close[i], self.entry_size, self.commission, self.commission_type
    #         )
    #         if self.commission_type == "percentage":
    #             # print("missing")
    #             a = 4
    #         else:
    #             fee = fee * 2
    #         # pnl = 0
    #         # for j in range(0, self.trade_idx):
    #         #     pnl += self.trades[j, 4]
    #         self.equity[i] = self.initial_capital + self.total_pnl
    #
    #     self.final_value = self.equity[-1]
    #     self.trades = self.trades[: self.trade_idx, :]
    #
    # def from_orders(self, size):
    #     print("need implementing")
    #     return
    #
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

    # def calculate_trade_exit_pnl(self, trade, exit_price):
    #     direction = trade[1]
    #     trade_price = trade[3]
    #     trade_volume = trade[6]
    #
    #     commission = 0
    #     if self.commission_type == "fixed":
    #         commission = self.commission
    #
    #     if direction == 1:  # LONG
    #         pnl = (exit_price - trade_price) * trade_volume - commission
    #     else:
    #         pnl = (trade_price - exit_price) * trade_volume - commission
    #     return pnl

    def check_trades_to_close(self, current_tick, index):
        for trade in self.active_trades:
            if trade[Trade.TIME_SL.value] < current_tick:
                print("need to close trade")
                direction = trade[Trade.Direction.value]
                exit_price = calculate_exit_price(
                    self.slippage, direction, None, self.bid[index], self.ask[index]
                )

                new_trade = trade
                new_trade[Trade.Active.value] = False
                new_trade[Trade.ExitPrice.value] = exit_price
                new_trade[Trade.PNL.value] = PNL.calculate_trade_exit_pnl(trade)

                self.closed_trades[self.last_closed_trade_index] = new_trade
                self.last_closed_trade_index += 1

                self.total_pnl = PNL.calculate_realized_pnl(self.closed_trades)

    #             self.update_active_trades()
    #
    #
    # def update_equity(self, index, active_trades):
    #     pnl = 0
    #     for trade in active_trades:
    #         # if index > 20008:
    #         #     print(pnl, "  --  ", trade[7])
    #         pnl += trade[7]
    #
    #     # if index > 20008:
    #     #     print(self.cash, self.total_pnl, pnl)
    #
    #     self.equity[index] = self.cash + self.total_pnl + pnl

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
        # print("Adding new trade")
        trade = create_new_trade(*args)
        self.active_trades[self.last_active_trade_index] = trade
        self.last_active_trade_index += 1

    def from_trades(self, trades):
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
                price = calculate_trade_price(
                    self.slippage, direction, None, self.bid[i], self.ask[i]
                )

                self.add_trade(
                    i, direction, curr_trade[0], price, volume, 0, 0, exit_time, 0
                )

            self.update_trades_pnl(i)
            self.check_trades_to_close(self.date[i], i)

        self.active_trades = self.active_trades[: self.last_active_trade_index]
        return 0
        #     if last_trade_index < len(trades):
        #         self.update_trades_pnl(i, self.active_trades)
        #         self.check_trades_to_close(self.date[i], i)
        #         self.update_equity(i, self.active_trades)
        #
        #         if self.was_trade_filled(i, self.date, curr_trade[0], debug=False):
        #             entry_time = curr_trade[0]
        #             exit_time = curr_trade[1]
        #             volume = curr_trade[2]
        #             direction = curr_trade[3]
        #
        #             if direction == 1:
        #                 price = self.ask[i]
        #             else:
        #                 price = self.bid[i]
        #
        #             commission = 0
        #             if self.commission_type == "fixed":
        #                 commission = self.commission
        #             self.trades[last_trade_index] = [
        #                 last_trade_index,
        #                 direction,
        #                 entry_time,
        #                 price + self.slippage,
        #                 exit_time,  # Exit Time
        #                 -1,  # Exit Price
        #                 volume,
        #                 0,  # PNL
        #                 commission,  # Need to implement commission
        #                 True,
        #             ]
        #             # print("Entering a trade")
        #             last_trade_index += 1
        #             self.update_active_trades()
        #
        # self.trades = self.trades[:last_trade_index]
        # self.closed_trades = self.closed_trades[: self.number_of_closed_trades]


# from quantnb.indicators.random_data import random_data
#
# date, open, high, low, close, df = random_data()
# bt = Backtester(
#     # open=open, high=high, low=low, close=close, date=date, data_type=DataType.OHLC
#     bid=open,
#     ask=close,
#     date=date,
#     data_type=DataType.BID_ASK,
# )
# bt
