"""
This is the Hull Moving Average.
It's formula is as follow:


HMA = WMA(2*WMA(n/2) − WMA(n)),sqrt(n))

"""
import talib
import numpy as np


def HMA(close_prices, HMA_Period=33):
    return talib.WMA(
        2 * talib.WMA(close_prices, int(HMA_Period / 2))
        - talib.WMA(close_prices, HMA_Period),
        int(np.sqrt(HMA_Period)),
    )
