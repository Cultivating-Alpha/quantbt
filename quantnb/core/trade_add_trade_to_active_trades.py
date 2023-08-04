import numpy as np
from numba import njit
from numpy import ndarray
from quantnb.core.enums import Trade

TRADE_ITEMS_COUNT = Trade.__len__()


@njit(cache=True)
def add_trade_to_active_trades(active_trades, trade) -> ndarray:
    new_active_trades: ndarray = np.zeros(
        (len(active_trades) + 1, TRADE_ITEMS_COUNT), dtype=np.float64
    )

    for i in range(len(active_trades)):
        new_active_trades[i] = active_trades[i]
    new_active_trades[len(active_trades)] = trade

    return new_active_trades
