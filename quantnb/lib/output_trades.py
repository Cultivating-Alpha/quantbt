import pandas as pd
import numpy as np


def output_trades(bt, concatenate=True):
    trades = bt.trades
    if concatenate:
        trades = np.concatenate((bt.closed_trades, bt.active_trades))

    trades = pd.DataFrame(
        trades,
        # bt.trades,
        columns=[
            "Index",
            "Direction",
            "EntryTime",
            "EntryPrice",
            "ExitTime",
            "ExitPrice",
            "Volume",
            "PNL",
            "Commission",
            "Active",
        ],
    )

    trades["EntryTime"] = pd.to_datetime(trades["EntryTime"], unit="s")
    trades["ExitTime"] = pd.to_datetime(trades["ExitTime"], unit="s")
    return trades
