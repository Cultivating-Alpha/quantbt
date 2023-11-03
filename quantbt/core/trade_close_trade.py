from numba import njit
from quantbt.core.enums import Trade, PositionCloseReason, OrderDirection
from quantbt.core.calculate_exit_price import calculate_exit_price


@njit
def close_trade(
    trade, slippage, price_value, bid, ask, current_tick, close_reason, multiplier
) -> tuple[dict, float, int]:
    # GENERATE DEBUG
    direction = trade[Trade.Direction.value]
    volume = trade[Trade.Volume.value]
    entry_price = trade[Trade.EntryPrice.value]

    if close_reason == PositionCloseReason.SL.value:
        exit_price = calculate_exit_price(
            slippage, direction, trade[Trade.SL.value], bid, ask
        )
    elif close_reason == PositionCloseReason.TSL.value:
        exit_price = calculate_exit_price(
            slippage, direction, trade[Trade.TSL.value], bid, ask
        )
    else:
        exit_price = calculate_exit_price(slippage, direction, price_value, bid, ask)

    new_pnl = 0
    if direction == OrderDirection.LONG.value:
        new_pnl = (exit_price - entry_price) * volume * multiplier - trade[
            Trade.Commission.value
        ]
    else:
        new_pnl = (entry_price - exit_price) * volume * multiplier - trade[
            Trade.Commission.value
        ]

    trade[Trade.ExitPrice.value] = exit_price
    trade[Trade.ExitTime.value] = current_tick
    trade[Trade.Active.value] = False
    trade[Trade.CloseReason.value] = close_reason

    # Update Closed PNL
    trade[Trade.PNL.value] = new_pnl
    new_pnl = trade[Trade.PNL.value]

    # Set Active state of trade
    index = int(trade[Trade.IDX.value])

    return trade, new_pnl, index
