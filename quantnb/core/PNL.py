from quantnb.core.enums import OrderDirection, Trade, DataType
from quantnb.core import calculate_commission
from numba import njit


@njit
def update_trades_pnl(
    active_trades,
    last_active_trade_index,
    commission=0,
    commission_type="fixed",
    data_type=0,
    price_value=None,
    bid=None,
    ask=None,
):
    for i in range(0, last_active_trade_index):
        trade = active_trades[i]
        direction = trade[Trade.Direction.value]
        entry_price = trade[Trade.EntryPrice.value]
        trade_volume = trade[Trade.Volume.value]

        if direction == OrderDirection.LONG.value:
            if data_type == DataType.OHLC:
                price = price_value
            else:
                price = bid
            commission = calculate_commission(commission_type, commission, price)
            pnl = (price - entry_price) * trade_volume - commission
        else:
            if data_type == DataType.OHLC.value:
                price = price_value
            else:
                price = ask
            commission = calculate_commission(commission_type, commission, price)
            pnl = (entry_price - price) * trade_volume - commission

        active_trades[i][Trade.PNL.value] = pnl
    return active_trades


@njit
def calculate_trade_exit_pnl(trade):
    direction = trade[Trade.Direction.value]
    entry_price = trade[Trade.EntryPrice.value]
    exit_price = trade[Trade.ExitPrice.value]
    trade_volume = trade[Trade.Volume.value]
    commission = trade[Trade.Commission.value]

    if direction == OrderDirection.LONG.value:
        pnl = (exit_price - entry_price) * trade_volume - commission
    else:
        pnl = (entry_price - exit_price) * trade_volume - commission
    return pnl


@njit
def calculate_realized_pnl(closed_trades):
    realized_pnl = 0
    for trade in closed_trades:
        realized_pnl += trade[Trade.PNL.value]
    return realized_pnl
