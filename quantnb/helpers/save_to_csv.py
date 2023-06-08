import numpy as np
import pandas as pd


def save_to_csv(pf, data, signal, indicators, strategy, name="TEST"):
    df = data.copy()
    df["i"] = i
    df["i2"] = i2
    df["dd"] = signal
    df["rsi"] = rsi
    df["atr"] = atr

    df["e"] = equity

    short_orders = np.full_like(data.Close, 0, dtype=float)
    long_orders = np.full_like(data.Close, 0, dtype=float)

    for order in orders_arr:
        index = int(order[0])
        if order[1] == -1:
            short_orders[index] = order[2]
        else:
            long_orders[index] = order[2]
    df["short_order"] = short_orders
    df["long_order"] = long_orders

    df[200 - 1 :].to_csv(
        f"/home/alpha/workspace/cultivating-alpha/UI/public/TEST.csv"
    )
