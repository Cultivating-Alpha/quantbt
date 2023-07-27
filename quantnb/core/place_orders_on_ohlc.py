import numpy as np
from numba import njit
import pandas as pd
from ..lib.time_manip import time_manip


@njit
def places_orders_on_ohlc_nb(ohlc, order, vol, debug=True):
    new_array = np.zeros((ohlc.shape[0], 2), dtype=np.float32)

    last_trade_index = 0

    for i in range(len(ohlc)):
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

    print("Last trade index: ", last_trade_index)
    # print(array2[last_trade_index])
    return new_array


def place_orders_on_ohlc(ohlc, orders, bid_column, ask_column):
    """
    Places orders on OHLC data and returns the result.

    Parameters:
        ohlc (pd.DataFrame): DataFrame containing OHLC data with timestamps as the index.
        orders (pd.DataFrame): DataFrame containing order data with 'time' and 'volume' columns.
        bid_column (str): Name of the column in 'ohlc' DataFrame representing bid prices.
        ask_column (str): Name of the column in 'ohlc' DataFrame representing ask prices.

    Returns:
        pd.DataFrame: A DataFrame with columns 'Date', 'Bid', and 'Ask'.
        ndarray: An array containing the processed order data.

    Usage:
        ohlc_data, orders_data = place_orders_on_ohlc(ohlc_df, orders_df, 'EURUSD.bid', 'EURUSD.ask')

    Example:
        >> place_orders_on_ohlc(ohlc_df, orders_df, 'EURUSD.bid', 'EURUSD.ask')
        << (ohlc_data, orders_data)
    """
    data = pd.DataFrame(
        {
            "Date": time_manip.convert_datetime_to_ms(ohlc.index),
            "Bid": ohlc[bid_column].values,
            "Ask": ohlc[ask_column].values,
        }
    )

    orders_data_array = places_orders_on_ohlc_nb(
        data["Date"].values,
        orders["time"].values,
        orders["volume"].values,
        debug=False,
    )
    return data, orders_data_array
