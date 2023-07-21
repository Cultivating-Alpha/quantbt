import pandas as pd


def calculate_stats(data, bt):
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
    trades["EntryTime"] = pd.to_datetime(trades["EntryTime"], unit="ms")
    trades["ExitTime"] = pd.to_datetime(trades["ExitTime"], unit="ms")
    trades["Duration"] = trades["ExitTime"] - trades["EntryTime"]

    first_data_day = data["Date"].iloc[0]
    last_data_day = data["Date"].iloc[-1]
    total_trading_days = (last_data_day - first_data_day).total_seconds() / (24 * 3600)

    ROI = bt.equity[-1] / bt.cash
    ROI_usd = bt.equity[-1] - bt.cash
    biggest_winning_trade = trades["PNL"].max()
    biggest_losing_trade = trades["PNL"].min()
    longest_held_trade = trades["Duration"].max()
    shortest_held_trade = trades["Duration"].min()
    average_held_trade = trades["Duration"].mean()
    largest_trade_volume = trades["Volume"].max()
    smallest_trade_volume = trades["Volume"].min()
    average_number_of_trades_per_day = len(trades) / total_trading_days

    print("ROI: (%)", ROI)
    print("ROI: ($)", ROI_usd)
    print("Biggest winning trade: ($)", biggest_winning_trade)
    print("Biggest losing trade: ($)", biggest_losing_trade)
    print("Longest held trade:", longest_held_trade)
    print("Shortest held trade:", shortest_held_trade)
    print("Average held trade:", average_held_trade)
    print("Largest trade volume: ($)", largest_trade_volume)
    print("Smallest trade volume: ($)", smallest_trade_volume)
    print("Total Trading days: ", total_trading_days)
    print("Total Trades: ", len(trades))
    print("Closed Trades: ", len(bt.closed_trades))
    print("Average number of trades per day: ", average_number_of_trades_per_day)
