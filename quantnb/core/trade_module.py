import numpy as np
from typing import List
from numba.experimental import jitclass
from quantnb.core.specs_nb import trade_specs
from quantnb.core.PNL import update_trades_pnl
from quantnb.core.trade_create_new_trade import create_new_trade
from quantnb.core.enums import (
    Trade,
    DataType,
    OrderDirection,
    OrderType,
    CommissionType,
)

from quantnb.core.calculate_exit_price import calculate_exit_price
from quantnb.core.trade_remove_from_active_trades import remove_from_active_trades
from quantnb.core.trade_add_trade_to_active_trades import add_trade_to_active_trades
from quantnb.core.trade_close_trade import close_trade
from quantnb.core.trade_should_trade_close import should_trade_close

TRADE_ITEMS_COUNT = Trade.__len__()


# pyright: reportGeneralTypeIssues=false
@jitclass(trade_specs)
class TradeModule:
    def __init__(
        self,
        multiplier=1,
        data_type=DataType.OHLC.value,
        slippage=0.0,
        commission=0.0,
        commission_type=CommissionType.FIXED.value,
        max_active_trades=100,
        max_closed_trades=100000,
    ) -> None:
        # Arrays
        self.closed_trades: List[float] = np.zeros(
            (max_closed_trades, TRADE_ITEMS_COUNT), dtype=np.float64
        )
        self.active_trades: List[float] = np.zeros(
            (0, TRADE_ITEMS_COUNT), dtype=np.float64
        )

        self.last_closed_trade_index: int = 0
        self.last_trade_index: int = 0
        self.multiplier: int = multiplier
        self.data_type: int = data_type
        self.max_active_trades: int = max_active_trades

        # COMMISSIONS
        self.commission: float = commission
        self.commission_type: int = commission_type

        # SLIPPAGE
        self.slippage: float = slippage

        # PNL
        self.floating_pnl: float = 0.0
        self.closed_pnl: float = 0.0

    # ============================================================================= #
    #                                PNL FUNCTIONS                                  #
    # ============================================================================= #
    def update_trades_pnl(self, price_value, bid, ask):
        self.floating_pnl = update_trades_pnl(
            self.active_trades,
            commission=self.commission,
            commission_type=self.commission_type,
            multiplier=self.multiplier,
            slippage=self.slippage,
            price_value=price_value,
            bid=bid,
            ask=ask,
        )

    def reconcile(self):
        self.closed_trades = self.closed_trades[: self.last_closed_trade_index]

    # ============================================================================= #
    #                               LOOP FUNCTIONS                                  #
    # ============================================================================= #
    def close_trade(self, trade, price_data, close_reason):
        current_tick, price_value, bid, ask = price_data
        trade, new_pnl, index = close_trade(
            trade, self.slippage, price_value, bid, ask, current_tick, close_reason
        )

        # Update Closed Trades
        self.closed_trades[self.last_closed_trade_index] = trade
        self.last_closed_trade_index += 1
        #
        # Update Closed PNL
        self.closed_pnl += new_pnl

        # Set Active state of trade
        self.active_trades = remove_from_active_trades(self.active_trades, index)

    def check_trades_to_close(self, price_data):
        if len(self.active_trades) == 0:
            return

        for trade in self.active_trades:
            need_to_close, close_reason = should_trade_close(trade, price_data)

            if need_to_close:
                self.close_trade(trade, price_data, close_reason)
        return

    def add_trade(
        self,
        index,
        direction=OrderDirection.LONG.value,
        order_type=OrderType.MARKET.value,
        entry_time=0.0,
        entry_price=0.0,
        volume=0.0,
        tp=0.0,
        sl=0.0,
        time_sl=np.inf,
        extra=-1,
    ) -> None:
        if len(self.active_trades) >= self.max_active_trades:
            # DEBUG
            debug = True
            print(
                "You have reached the max amount of trades. Please increase the max_active_trades property"
            )
        else:
            if order_type == OrderType.MARKET.value:
                trade = create_new_trade(
                    self.last_trade_index,
                    index,
                    direction,
                    entry_time,
                    entry_price,
                    volume,
                    tp,
                    sl,
                    time_sl,
                    self.commission,
                    extra,
                )

                self.active_trades = add_trade_to_active_trades(
                    self.active_trades, trade
                )
                self.last_trade_index += 1

            # elif order_type == OrderType.STOP_LIMIT.value:
            #     was_order_hit(
