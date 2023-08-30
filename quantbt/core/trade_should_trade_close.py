from numba import njit
import numpy as np

from quantbt.core.enums import Trade
from quantbt.core.enums import PositionCloseReason, OrderDirection


@njit(cache=True)
def should_trade_close(trade, price_data):
    current_tick, price_value, low, high = price_data
    if trade[Trade.TIME_SL.value] < current_tick:
        return True, PositionCloseReason.TIME_SL.value
    if trade[Trade.SL.value] != 0:
        if trade[Trade.Direction.value] == OrderDirection.LONG.value:
            if trade[Trade.SL.value] >= low:
                return True, PositionCloseReason.SL.value
        else:
            if trade[Trade.SL.value] <= high:
                return True, PositionCloseReason.SL.value
    if trade[Trade.TSL.value] != np.inf:
        if trade[Trade.Direction.value] == OrderDirection.LONG.value:
            if trade[Trade.TSL.value] >= low:
                return True, PositionCloseReason.TSL.value
        else:
            if trade[Trade.TSL.value] <= high:
                return True, PositionCloseReason.TSL.value
    # elif trade[Trade.TP.value] != 0:
    #     # print("CHECK TP")
    #     return True, PositionCloseReason.TP.value

    # GENERATE DEBUG
    # print("What to do when TP and SL is hit in the same candle")
    return False, None
