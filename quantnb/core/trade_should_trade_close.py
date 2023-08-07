from numba import njit

from quantnb.core.enums import Trade
from quantnb.core.enums import PositionCloseReason


@njit(cache=True)
def should_trade_close(trade, price_data):
    current_tick, price_value, bid, ask = price_data
    if trade[Trade.TIME_SL.value] < current_tick:
        return True, PositionCloseReason.TIME_SL.value
    # elif trade[Trade.SL.value] != 0:
    #     # print("CHECK SL")
    #     return True, PositionCloseReason.SL.value
    # elif trade[Trade.TP.value] != 0:
    #     # print("CHECK TP")
    #     return True, PositionCloseReason.TP.value

    # GENERATE DEBUG
    # print("What to do when TP and SL is hit in the same candle")
    return False, None
