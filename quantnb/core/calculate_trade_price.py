from quantnb.core.enums import OrderDirection
from numba import njit


@njit
def calculate_trade_price(slippage, direction, price_value=None, bid=None, ask=None):
    if price_value is not None:
        entry_price = price_value
    else:
        if direction == OrderDirection.LONG.value:
            entry_price = ask
        else:
            entry_price = bid

    if direction == OrderDirection.LONG.value:
        entry_price += slippage
    else:
        entry_price -= slippage
    return entry_price
