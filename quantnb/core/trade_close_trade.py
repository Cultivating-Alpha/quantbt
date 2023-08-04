from numba import njit
from quantnb.core.enums import Trade
from quantnb.core.calculate_exit_price import calculate_exit_price


@njit(cache=True)
def close_trade(
    trade, slippage, price_value, bid, ask, current_tick, close_reason
) -> tuple[dict, float, int]:
    # GENERATE DEBUG
    # print("Should close trade")
    # print(trade[Trade.Index.value])
    # print(trade[Trade.IDX.value])
    direction = trade[Trade.Direction.value]
    exit_price = calculate_exit_price(slippage, direction, price_value, bid, ask)
    # print("==========")
    # print(self.slippage)
    # print(price_value)
    # print(exit_price)

    trade[Trade.ExitPrice.value] = exit_price
    trade[Trade.ExitTime.value] = current_tick
    trade[Trade.Active.value] = False
    trade[Trade.CloseReason.value] = close_reason

    # Update Closed PNL
    new_pnl = trade[Trade.PNL.value]

    # Set Active state of trade
    index = int(trade[Trade.IDX.value])

    return trade, new_pnl, index
