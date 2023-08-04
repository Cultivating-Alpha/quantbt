import numpy as np
from numba import njit
from numpy import ndarray
from quantnb.core.enums import Trade

TRADE_ITEMS_COUNT = Trade.__len__()


@njit(cache=True)
def remove_from_active_trades(active_trades: ndarray, index: int) -> ndarray:
    new_active_trades: ndarray = np.zeros(
        (len(active_trades), TRADE_ITEMS_COUNT), dtype=np.float64
    )
    count: int = 0
    for i in range(len(active_trades)):
        trade = active_trades[i]
        if trade[Trade.IDX.value] != index:
            new_active_trades[count] = trade
            count += 1

    if count == 0:
        return np.zeros((0, TRADE_ITEMS_COUNT), dtype=np.float64)
    else:
        return new_active_trades[:count]
