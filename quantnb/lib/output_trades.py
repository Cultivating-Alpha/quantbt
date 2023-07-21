import pandas as pd


def output_trades(bt):
    trades = pd.DataFrame(
        bt.trades,
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
