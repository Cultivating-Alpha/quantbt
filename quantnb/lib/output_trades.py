import pandas as pd
import numpy as np
from quantnb.core.enums import CommissionType, Trade


TRADE_ITEMS_COUNT = Trade.__len__()

all_names = [trade.name for trade in Trade]
all_names


def output_trades(bt, unit="ms"):
    # trades = np.concatenate((bt.closed_trades, bt.active_trades))
    trades = bt.active_trades

    trades = pd.DataFrame(
        trades,
        columns=all_names,
    )
    print(trades)

    trades["EntryTime"] = pd.to_datetime(trades["EntryTime"], unit=unit)
    trades["ExitTime"] = pd.to_datetime(trades["ExitTime"], unit=unit)
    return trades
