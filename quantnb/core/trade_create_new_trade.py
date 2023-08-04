import numpy as np
from numba import float32, int32, int64, float64, njit
from quantnb.core.enums import Trade
from quantnb.core.enums import CommissionType

from quantnb.core.calculate_commission import calculate_commission

TRADE_ITEMS_COUNT = Trade.__len__()


@njit(cache=True)
def create_new_trade(
    idx,
    index,
    direction,
    entry_time,
    entry_price,
    volume=0,
    tp=0,
    sl=0,
    time_sl=np.inf,
    commission=0,
    extra=0,
) -> np.ndarray:
    trade = np.empty(TRADE_ITEMS_COUNT, dtype=np.float64)

    trade[Trade.IDX.value] = idx
    trade[Trade.Index.value] = index
    trade[Trade.Direction.value] = direction
    trade[Trade.EntryTime.value] = entry_time
    trade[Trade.EntryPrice.value] = entry_price
    trade[Trade.ExitTime.value] = -1
    trade[Trade.ExitPrice.value] = -1
    trade[Trade.Volume.value] = volume
    trade[Trade.TP.value] = tp
    trade[Trade.SL.value] = sl
    trade[Trade.TIME_SL.value] = time_sl
    trade[Trade.PNL.value] = commission * -1
    trade[Trade.Commission.value] = commission
    trade[Trade.Active.value] = True
    trade[Trade.Extra.value] = extra
    trade[Trade.CloseReason.value] = -1

    return trade
