from quantbt.core.enums import OrderDirection
from numba import njit


@njit
def calculate_exit_price(slippage, direction, price_value=0.0, bid=0.0, ask=0.0):
    if direction == OrderDirection.LONG.value:
        if price_value > 0:
            exit_price = price_value - slippage
        else:
            exit_price = bid - slippage
    else:
        if price_value > 0:
            exit_price = price_value + slippage
        else:
            exit_price = ask + slippage

    return exit_price
