import pandas as pd


def print_trades(trades_arr):
    trades_df = pd.DataFrame(
        trades_arr,
        columns=[
            "entry_time",
            "exit_time",
            "entry_price",
            "exit_price",
            "pnl",
            "size",
            "direction",
        ],
    )
    # Mapping dictionary for column renaming
    rename_dict = {1: "LONG", 0: "SHORT"}

    trades_df["direction"] = trades_df["direction"].replace({1: "LONG", 0: "SHORT"})
    # Rename columns using the mapping dictionary
    trades_df["entry_time"] = pd.to_datetime(trades_df["entry_time"], unit="s")
    trades_df["exit_time"] = pd.to_datetime(trades_df["exit_time"], unit="s")
    print(trades_df)
    return trades_df
