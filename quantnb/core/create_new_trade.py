from quantnb.core.enums import CommissionType, Trade
from quantnb.core import calculate_commission
from numba import njit
import numpy as np

TRADE_ITEMS_COUNT = Trade.__len__()


@njit(cache=True)
def create_new_trade(
    active_trades,
    last_active_trade_index,
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

    # new_trades = np.zeros(
    #     (last_active_trade_index, TRADE_ITEMS_COUNT), dtype=np.float64
    # )
    #
    # for i in range(len(active_trades)):
    #     new_trades[i] = active_trades[i]
    # Copy the first (last_active_trade_index - 1) rows from active_trades to new_trades

    new_trades = np.empty(
        (last_active_trade_index, TRADE_ITEMS_COUNT), dtype=np.float64
    )
    new_trades[: last_active_trade_index - 1] = active_trades[
        : last_active_trade_index - 1
    ]

    # Assign the trade data to the last row of new_trades
    # new_trades[last_active_trade_index - 1] = trade
    new_trades[last_active_trade_index - 1] = trade

    return new_trades
