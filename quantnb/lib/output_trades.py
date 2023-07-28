import pandas as pd
import numpy as np


def output_trades(bt):
    trades = np.concatenate((bt.closed_trades, bt.active_trades))
    # trades = bt.trades
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
    return trades
