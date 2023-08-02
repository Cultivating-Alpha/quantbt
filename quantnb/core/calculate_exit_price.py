from quantnb.core.enums import OrderDirection
from numba import njit


@njit
def calculate_exit_price(slippage, direction, price_value=None, bid=None, ask=None):
    if price_value is not None:
        exit_price = price_value
    else:
        if direction == OrderDirection.LONG.value:
            exit_price = bid
        else:
            exit_price = ask

    if slippage is not None:
        if direction == OrderDirection.LONG.value:
            exit_price += slippage
        else:
            exit_price -= slippage

    return exit_price
