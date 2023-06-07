import numpy as np
import pandas as pd


def calculate_metrics(equity, data, final_value):
    prices = pd.Series(equity, index=data.index)

    dd = prices / np.maximum.accumulate(prices) - 1.0
    dd = dd.replace([np.inf, -np.inf, -0], 0).min()
    dd = dd * 100

    total_return = ((final_value / 10000) - 1) * 100
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
