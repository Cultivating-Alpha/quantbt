from numba import njit

from quantnb.core.enums import Trade
from quantnb.core.enums import PositionCloseReason, OrderDirection


@njit(cache=True)
def should_trade_close(trade, price_data):
    current_tick, price_value, low, high = price_data
    if trade[Trade.TIME_SL.value] < current_tick:
        return True, PositionCloseReason.TIME_SL.value
    elif trade[Trade.SL.value] != 0:
        if trade[Trade.Direction.value] == OrderDirection.LONG.value:
            if trade[Trade.SL.value] >= low:
                return True, PositionCloseReason.SL.value
        else:
            if trade[Trade.SL.value] <= high:
                print(trade[Trade.SL.value], price_value, high)
                return True, PositionCloseReason.SL.value
        return False, None
    # elif trade[Trade.TP.value] != 0:
    #     # print("CHECK TP")
    #     return True, PositionCloseReason.TP.value

    # GENERATE DEBUG
    # print("What to do when TP and SL is hit in the same candle")
    return False, None
