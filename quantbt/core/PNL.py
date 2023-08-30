from numba import njit
from typing import List, Tuple
from quantnb.core import calculate_commission
from quantnb.core.enums import (
    CommissionType,
    OrderDirection,
    Trade,
    DataType,
    CommissionType,
)
from quantnb.core.calculate_exit_price import calculate_exit_price


@njit
def update_trades_pnl(
    active_trades,
    commission=0,
    commission_type=CommissionType.FIXED,
    slippage=0,
    multiplier=1,
    price_value=0.0,
    bid=0.0,
    ask=0.0,
) -> float:
    cumulative_pnl = 0.0
    for i in range(len(active_trades)):
        # General Data on the Trade
        trade = active_trades[i]
        direction = trade[Trade.Direction.value]
        entry_price = trade[Trade.EntryPrice.value]
        trade_volume = trade[Trade.Volume.value]

        # Calculate the PNL
        current_price = calculate_exit_price(slippage, direction, price_value, bid, ask)
        trade_commission = calculate_commission(
            commission_type, commission, current_price, entry_price, trade_volume
        )
        if direction == OrderDirection.LONG.value:
            pnl = ((current_price - entry_price) * trade_volume) * multiplier
            pnl -= trade_commission
        else:
            pnl = ((entry_price - current_price) * trade_volume) * multiplier
            pnl -= trade_commission

        # Update Metrics
        cumulative_pnl += pnl
        active_trades[i][Trade.PNL.value] = pnl
        active_trades[i][Trade.Commission.value] = trade_commission
    # return active_trades, cumulative_pnl
    return cumulative_pnl


# @njit(cache=True)
# def calculate_trade_exit_pnl(trade):
#     direction = trade[Trade.Direction.value]
#     entry_price = trade[Trade.EntryPrice.value]
#     exit_price = trade[Trade.ExitPrice.value]
#     trade_volume = trade[Trade.Volume.value]
#     commission = trade[Trade.Commission.value]
#
#     if direction == OrderDirection.LONG.value:
#         pnl = (exit_price - entry_price) * trade_volume - commission
#     else:
#         pnl = (entry_price - exit_price) * trade_volume - commission
#     return pnl
#
#
# @njit(cache=True)
# def calculate_realized_pnl(closed_trades):
#     realized_pnl = 0
#     for trade in closed_trades:
#         realized_pnl += trade[Trade.PNL.value]
#     return realized_pnl
