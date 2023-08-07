import pandas as pd
import numpy as np
from quantnb.core.enums import CommissionType, Trade


TRADE_ITEMS_COUNT = Trade.__len__()

all_names = [trade.name for trade in Trade]
all_names


def output_trades(bt, unit="ms"):
    trade_module = bt.trade_module
    trades = np.concatenate((trade_module.closed_trades, trade_module.active_trades))
    # trades = bt.active_trades

    trades = pd.DataFrame(
        trades,
        columns=all_names,
    )
    trades["EntryTime"] = pd.to_datetime(trades["EntryTime"], unit=unit)
    trades["ExitTime"] = pd.to_datetime(trades["ExitTime"], unit=unit)
    # trades["TIME_SL"] = pd.to_datetime(trades["TIME_SL"], unit=unit)

    closed_trades = trades[trades["Active"] == 0]
    active_trades = trades[trades["Active"] == 1]
    return trades, closed_trades, active_trades
