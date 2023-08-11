import pandas as pd
from prettytable import PrettyTable
from .output_trades import output_trades
import numpy as np
from numba import njit


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


def calculate_cagr(beginning_value, ending_value, num_years):
    cagr = (ending_value / beginning_value) ** (1 / num_years) - 1
    return cagr


@njit(cache=True)
def calculate_dd(equity):
    # Assuming equity is your numpy array (already a NumPy array in the original code)

    # Calculate the running maximum
    running_max = np.empty_like(equity)
    current_max = -np.inf
    for i in range(len(equity)):
        current_max = max(current_max, equity[i])
        running_max[i] = current_max

    # Calculate the drawdown as the difference between the running max and the current equity
    drawdown = running_max - equity

    # Calculate the maximum drawdown
    max_drawdown = drawdown.max()

    # Identify the peak value that precedes the maximum drawdown
    max_drawdown_index = np.argmax(drawdown)
    peak_before_max_drawdown = running_max[max_drawdown_index]

    # Calculate the maximum drawdown as a percentage
    max_drawdown_pct = max_drawdown / peak_before_max_drawdown * 100
    return max_drawdown_pct


def calculate_stats(
    data, trades, closed_trades, equity, initial_capital, display=True, index=None
):
    t = PrettyTable(["Label", "Value"])

    closed_trades["Duration"] = closed_trades["ExitTime"] - closed_trades["EntryTime"]

    first_data_day = data["Date"].iloc[0]
    last_data_day = data["Date"].iloc[-1]
    total_trading_days = np.round(
        (last_data_day - first_data_day).total_seconds() / (24 * 3600)
    )

    equity = equity
    initial_capital = initial_capital

    dd = np.round(calculate_dd(equity), 2)

    ROI = np.round((equity[-1] - initial_capital) / initial_capital * 100, 2)
    ROI_usd = np.round(equity[-1] - initial_capital, 1)
    biggest_winning_trade = np.round(trades["PNL"].max(), 0)
    biggest_losing_trade = np.round(trades["PNL"].min(), 0)
    longest_held_trade = format_duration(closed_trades["Duration"].max())
    shortest_held_trade = format_duration(closed_trades["Duration"].min())
    average_held_trade = format_duration(closed_trades["Duration"].mean())
    largest_trade_volume = np.round(trades["Volume"].max(), 3)
    smallest_trade_volume = np.round(trades["Volume"].min(), 3)
    average_number_of_trades_per_day = np.round(len(trades) / total_trading_days, 3)

    cagr = calculate_cagr(equity[0], equity[-1], total_trading_days / 365)

    t.add_row(["Initial Capital", initial_capital])
    t.add_row(["End Value", equity[-1]])
    t.add_row(["Total Trading days: ", total_trading_days])
    t.add_row(["", ""])

    t.add_row(["ROI: (%)", f"{ROI}%"])
    t.add_row(["ROI: ($)", f"{ROI_usd}$"])
    t.add_row(["DD: (%)", f"{dd}"])
    t.add_row(["Biggest winning trade: ($)", f"{biggest_winning_trade}$"])
    t.add_row(["Biggest losing trade: ($)", f"{biggest_losing_trade}$"])
    t.add_row(["", ""])

    t.add_row(["Longest winning streak", winning_streak(trades)])
    t.add_row(["Longest losing streak", losing_streak(trades)])

    t.add_row(["Longest held trade:", longest_held_trade])
    t.add_row(["Shortest held trade:", shortest_held_trade])
    t.add_row(["Average held trade:", average_held_trade])
    t.add_row(["Largest trade volume: ($)", largest_trade_volume])
    t.add_row(["Smallest trade volume: ($)", smallest_trade_volume])
    t.add_row(["Total Trades: ", len(trades)])
    t.add_row(["Closed Trades: ", len(closed_trades)])
    t.add_row(["Average number of trades per day: ", average_number_of_trades_per_day])
    t.add_row(["", ""])
    t.add_row(["CAGR: ", f"{cagr:.2%}"])

    t.align = "l"

    if display:
        print(t)

    if index == None:
        index = [0]
    stats = pd.DataFrame(
        {"End Value": equity[-1], "ROI: (%)": ROI, "DD": dd, "ratio": ROI / dd},
        index=index,
    )
    return stats
