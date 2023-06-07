import numpy as np
import pandas as pd

import talib
import matplotlib.pyplot as plt


def EMA(data, period):
    return talib.MA(data, timeperiod=period, matype=talib.MA_Type.EMA)


def SMA(data, period):
    return talib.MA(data, timeperiod=period, matype=talib.MA_Type.SMA)


def cross_below(arr1, arr2):
    cross_below_mask = np.logical_and(arr1[:-1] > arr2[:-1], arr1[1:] < arr2[1:])
    return cross_below_mask


### Printing
def print_orders(orders_arr):
    # Convert the numpy arrays to dataframes
    orders_df = pd.DataFrame(
        orders_arr, columns=["timestamp", "action", "price", "size", "cash"]
    )
    orders_df["action"] = orders_df["action"].apply(
        lambda x: "buy" if x == 1 else "sell"
    )
    print(orders_df)


def print_trades(trades_arr):
    trades_df = pd.DataFrame(
        trades_arr,
        columns=["entry_time", "exit_time", "entry_price", "exit_price", "pnl", "size"],
    )
    trades_df["entry_time"] = pd.to_datetime(trades_df["entry_time"], unit="s")
    trades_df["exit_time"] = pd.to_datetime(trades_df["exit_time"], unit="s")
    pnl = trades_df["pnl"].sum()
    print(trades_df)
    # print('==========')
    # print(pnl)
    # print('==========')


#######
def plot_equity(equity, data):
    returns = pd.Series(equity, index=data.index)
    # returns = returns[returns > 100]
    returns.plot()
    plt.show()


#######


def calculate_metrics(equity, data, final_value):
    prices = pd.Series(equity, index=data.index)

    dd = prices / np.maximum.accumulate(prices) - 1.0
    dd = dd.replace([np.inf, -np.inf, -0], 0).min()
    dd = dd * 100

    total_return = ((final_value / 10000) - 1) * 100
    ratio = total_return / abs(dd)

    buy_and_hold = ((data.Close[-1] / data.Close[0]) - 1) * 100
    # print("Buy and hold: ", buy_and_hold)
    # initial_investment = 10000  # Example initial investment amount
    #
    # # Calculate the buy and hold strategy in dollar figures
    # buy_and_hold = (data["Close"] / data["Close"].iloc[0]) * initial_investment
    # print("Buy and hold: ", buy_and_hold)

    return dd, total_return, ratio, buy_and_hold
