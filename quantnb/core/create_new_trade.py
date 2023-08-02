from quantnb.core.enums import CommissionType, Trade
from quantnb.core import calculate_commission
from numba import njit

TRADE_ITEMS_COUNT = Trade.__len__()


# @njit
def create_new_trade(
    index,
    direction,
    entry_time,
    entry_price,
    volume,
    tp=0,
    sl=0,
    time_sl=None,
    extra=None,
    commission=0,
    commission_type=CommissionType.FIXED,
):
    commission = calculate_commission(commission_type, commission, entry_price)

    trade = [0] * TRADE_ITEMS_COUNT
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

    return trade
