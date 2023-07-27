import numpy as np
import pandas as pd


def calculate_dd(equity):
    # Assuming pf.equity is your numpy array
    equity = pd.Series(equity)

    # Calculate the running maximum
    running_max = equity.cummax()

    # Calculate the drawdown as the difference between the running max and the current equity
    drawdown = running_max - equity

    # Calculate the maximum drawdown
    max_drawdown = drawdown.max()

    # Identify the peak value that precedes the maximum drawdown
    peak_before_max_drawdown = running_max[drawdown.idxmax()]

    # Calculate the maximum drawdown as a percentage
    max_drawdown_pct = max_drawdown / peak_before_max_drawdown * 100
    return max_drawdown_pct


def calculate_metrics(equity, data, final_value, initial_capital):
    dd = calculate_dd(equity)

    total_return = ((final_value / initial_capital) - 1) * 100
    total_return = ((final_value / initial_capital) - 1) * 100
    total_return = final_value * 100 / initial_capital
    ratio = total_return / abs(dd)

    close = data.Close.values
    buy_and_hold = ((close[-1] / close[0]) - 1) * 100
    # print("Buy and hold: ", buy_and_hold)
    # initial_investment = 10000  # Example initial investment amount
    #
    # # Calculate the buy and hold strategy in dollar figures
    # buy_and_hold = (data["Close"] / data["Close"].iloc[0]) * initial_investment
    # print("Buy and hold: ", buy_and_hold)

    return dd, total_return, ratio, buy_and_hold
