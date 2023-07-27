import pandas as pd
from prettytable import PrettyTable
from .output_trades import output_trades
import numpy as np


def format_duration(duration):
    total_hours = duration.days * 24 + duration.seconds // 3600 - duration.days * 24
    return f"{duration.days} days and {total_hours} hours"


def losing_streak(trades):
    longest_streak = 0
    current_streak = 0
    for trade in trades.iterrows():
        if trade[1].PNL < 0:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 0
    return longest_streak


def winning_streak(trades):
    longest_streak = 0
    current_streak = 0
    for trade in trades.iterrows():
        if trade[1].PNL > 0:
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 0
    return longest_streak


def calculate_stats(data, bt):
    trades = output_trades(bt)
    t = PrettyTable(["Label", "Value"])

    trades["EntryTime"] = pd.to_datetime(trades["EntryTime"], unit="ms")
    trades["ExitTime"] = pd.to_datetime(trades["ExitTime"], unit="ms")
    trades["Duration"] = trades["ExitTime"] - trades["EntryTime"]

    first_data_day = data["Date"].iloc[0]
    last_data_day = data["Date"].iloc[-1]
    total_trading_days = np.round(
        (last_data_day - first_data_day).total_seconds() / (24 * 3600)
    )

    ROI = bt.equity[-1] / bt.cash
    ROI_usd = np.round(bt.equity[-1] - bt.cash, 3)
    biggest_winning_trade = np.round(trades["PNL"].max(), 0)
    biggest_losing_trade = np.round(trades["PNL"].min(), 0)
    longest_held_trade = format_duration(trades["Duration"].max())
    shortest_held_trade = format_duration(trades["Duration"].min())
    average_held_trade = format_duration(trades["Duration"].mean())
    largest_trade_volume = np.round(trades["Volume"].max(), 3)
    smallest_trade_volume = np.round(trades["Volume"].min(), 3)
    average_number_of_trades_per_day = np.round(len(trades) / total_trading_days, 3)

    t.add_row(["Initial Capital", bt.cash])
    t.add_row(["End Value", bt.equity[-1]])
    t.add_row(["Total Trading days: ", total_trading_days])
    t.add_row(["", ""])

    t.add_row(["ROI: (%)", np.round(ROI, 3)])
    t.add_row(["ROI: ($)", f"{ROI_usd}$"])
    t.add_row(["Biggest winning trade: ($)", f"{biggest_winning_trade}$"])
    t.add_row(["Biggest losing trade: ($)", f"{biggest_losing_trade}$"])

    t.add_row(["Longest winning streak", winning_streak(trades)])
    t.add_row(["Longest losing streak", losing_streak(trades)])

    t.add_row(["Longest held trade:", longest_held_trade])
    t.add_row(["Shortest held trade:", shortest_held_trade])
    t.add_row(["Average held trade:", average_held_trade])
    t.add_row(["Largest trade volume: ($)", largest_trade_volume])
    t.add_row(["Smallest trade volume: ($)", smallest_trade_volume])
    t.add_row(["Total Trades: ", len(trades)])
    t.add_row(["Closed Trades: ", len(bt.closed_trades)])
    t.add_row(["Average number of trades per day: ", average_number_of_trades_per_day])

    t.align = "l"
    print(t)
