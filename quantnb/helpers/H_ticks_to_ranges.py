import numpy as np
from numba import njit, jit
import numba as nb
import pandas as pd


@njit(cache=True)
def ticks_to_range(ticks, last_ohlc, range, range_type="value"):
    newdf = np.empty((len(ticks), 6), dtype=np.double)
    # newdf = np.empty((0, 6), dtype=np.double)
    start = last_ohlc[0]
    open = last_ohlc[1]
    high = last_ohlc[2]
    low = last_ohlc[3]
    close = last_ohlc[4]
    volume = 0

    original_range = range

    i = -1

    last_new_tick = 0

    for line in ticks:
        curr = line[1]

        tr = max(high - curr, curr - low)
        if range_type == "percent":
            range = curr * original_range / 100

        if tr > range:
            i += 1
            # Fix close to match either high or low
            close = low
            if curr > high:
                close = high

            # newarr = np.array(
            #     [[start, open, high, low, close, volume]], dtype=np.double
            # )
            # newdf = np.append(newdf, newarr, axis=0)
            print("======", volume)
            print(open)
            newdf[last_new_tick] = [start, open, high, low, close, volume]
            last_new_tick += 1
            start = line[0]
            open = curr
            high = curr
            low = curr
            close = curr
            volume = line[2]
        else:
            print("here")
            if curr > high:
                high = curr
            if curr < low:
                low = curr
            close = curr
            volume += line[2]

    newarr = np.array([[start, open, high, low, close, volume]], dtype=np.double)
    newdf = np.append(newdf, newarr, axis=0)
    print(last_new_tick)
    return newdf[:last_new_tick]


def df_from_ticks(newdf):
    df = pd.DataFrame(newdf, columns=["Date", "Open", "High", "Low", "Close", "Volume"])
    df["Date"] = pd.to_datetime(
        df["Date"], unit="ms", origin="unix"
    )  # Convert unix to readable dates
    # df["Date"] = df["Date"] + pd.Timedelta("08:00:00")  # Convert to GMT+4
    df["TR"] = df["High"] - df["Low"]
    df["%"] = (df["High"] - df["Low"]) * 100 / df["High"]
    return df


# |%%--%%| <fE51sBr2QC|O2VxbyutFA>
#
# asset = "EURUSD"
# pips = np.array([5, 10, 15, 20, 25, 30])
# pips = pips * 0.0001
#
# # ===
# asset = "XBTUSD"
# pips = [0.2, 0.4, 0.5, 0.6, 0.8, 1, 1.5, 2, 3, 4, 5]
# # ===
#
# # ===
# df = pd.read_hdf(f"./data/{asset}.full.h5", key="ticks")
# df.reset_index(inplace=True)
#
# head = df.values[0]
# last_ohlc = [head[0], head[1], head[1], head[1], head[1]]
# step = 1
# values = df.values
# for step in pips:
#     df = ticks_to_range(values, last_ohlc, step, "percent")
#     # df = ticks_to_range(values, last_ohlc, step)
#     df = df_from_ticks(df)
#     # df.to_csv(f"/home/alpha/workspace/318-ui/public/TEST.csv")
#     df.set_index("Date", inplace=True)
#     df.to_hdf(f"./data/{asset}/{step}.h5", key="ranges")
