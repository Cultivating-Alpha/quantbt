from quantnb.core.enums import OrderDirection
from numba import njit


@njit(cache=True)
def calculate_exit_price(slippage, direction, price_value=0.0, bid=0.0, ask=0.0):
    if direction == OrderDirection.LONG.value:
        if price_value > 0:
            entry_price = price_value - slippage
        else:
            entry_price = bid - slippage
    else:
        if price_value > 0:
            entry_price = price_value + slippage
        else:
            entry_price = ask + slippage

    return entry_price
