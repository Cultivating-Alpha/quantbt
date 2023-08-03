import numpy as np
from typing import List
from numba.experimental import jitclass
from quantnb.core.specs_nb import trade_specs
from quantnb.core.trade_create_new_trade import create_new_trade
from quantnb.core.PNL import update_trades_pnl
from quantnb.core.enums import Trade, DataType, OrderDirection, OrderType

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
        commission_type=2,
        max_active_trades=100,
    ) -> None:
        # Arrays
        self.trades: List[float] = np.zeros(
            (max_active_trades, TRADE_ITEMS_COUNT), dtype=np.float64
        )
        self.closed_trades: List[float] = np.zeros(
            (max_active_trades, TRADE_ITEMS_COUNT), dtype=np.float64
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

    def reset_active_trades(self) -> None:
        self.active_trades: List[float] = np.zeros(
            (self.last_trade_index, TRADE_ITEMS_COUNT), dtype=np.float64
        )
        count: int = 0
        for i in range(len(self.trades)):
            trade = self.trades[i]
            if trade[Trade.Active.value] == True:
                self.active_trades[i] = trade
                count += 1
        self.active_trades = self.active_trades[:count]

    def update_trades_pnl(self, price_value, bid, ask):
        (self.active_trades, self.floating_pnl) = update_trades_pnl(
            self.active_trades,
            commission=self.commission,
            slippage=self.slippage,
            price_value=price_value,
            bid=bid,
            ask=ask,
        )

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
            print(
                "You have reached the max amount of trades. Please increase the max_active_trades property"
            )
        else:
            if order_type == OrderType.MARKET.value:
                trade = create_new_trade(
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

                self.trades[self.last_trade_index] = trade
                self.last_trade_index += 1

                self.reset_active_trades()

            # elif order_type == OrderType.STOP_LIMIT.value:
            #     was_order_hit(
