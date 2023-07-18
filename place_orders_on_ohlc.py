import numpy as np
from numba import njit
import pandas as pd


@njit
def places_orders_on_ohlc_nb(ohlc, order, vol, debug=True):
    new_array = np.zeros((ohlc.shape[0], 2), dtype=np.float32)

    last_trade_index = 0

    for i in range(len(ohlc) - 1):
        tick = ohlc[i]
        next_tick = ohlc[i + 1]

        last_trade = order[last_trade_index]
        if tick < last_trade <= next_tick:
            # The order will be placed on the next tick
            new_array[i] = [next_tick, vol[last_trade_index]]
            last_trade_index += 1

        elif last_trade < tick:
            if debug:
                print("Skippped tick", last_trade_index, last_trade, tick, next_tick, i)
            new_array[i] = [tick, vol[last_trade_index]]
            last_trade_index += 1
        else:
            new_array[i] = [tick, 0]

        # if last_trade_index > total_trades:
        #     break

    print(last_trade_index)
    # print(array2[last_trade_index])
    return new_array[:-1]


#
def place_orders_on_ohlc(ohlc, orders):
    data = pd.DataFrame(
        {
            "Date": ohlc.index.astype(np.int64) // 10**6,
            "Bid": ohlc["EURUSD.bid"].values,
            "Ask": ohlc["EURUSD.ask"].values,
        }
    )

    orders_data_array = places_orders_on_ohlc_nb(
        data["Date"].values,
        orders["time"].values,
        orders["volume"].values,
        debug=False,
    )
    return data, orders_data_array
