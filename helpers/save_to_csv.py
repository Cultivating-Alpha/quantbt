import numpy as np
import pandas as pd


def save_to_csv(pf, data, signal, indicators, strategy, name="TEST"):
    df = pd.DataFrame()
    df["Close"] = data.close
    df["Open"] = data.open
    df["High"] = data.high
    df["Low"] = data.low
    df["i"] = indicators[0]
    if len(indicators) > 1:
        df["i2"] = indicators[1]
    df["dd"] = signal

    df["e"] = pf.get_value()
    short_orders = np.full_like(pf.orders.mask, 0, dtype=float)
    long_orders = np.full_like(pf.orders.mask, 0, dtype=float)

    for order in pf.orders.records_arr:
        row = order[3]
        if order[8] == 1:
            short_orders[row] = order[6]
        else:
            long_orders[row] = order[6]
    df["short_order"] = short_orders
    df["long_order"] = long_orders
    df.to_csv(f"/home/alpha/workspace/318-ui/public/TEST.csv")
    # offset = 55 + 17 + 1
    # offset = 0
    # df[:100].to_csv(f"/home/alpha/workspace/318-ui/public/TEST.csv")
