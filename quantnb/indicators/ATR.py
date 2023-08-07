import numpy as np
from numba import jit
import talib


@jit(nopython=True, cache=True)
def true_range(high, low, close):
    # Calculate the True Range for each period
    high_low_diff = high - low
    high_close_diff = np.abs(high - close)
    low_close_diff = np.abs(low - close)
    true_range = np.maximum(high_low_diff, np.maximum(high_close_diff, low_close_diff))
    return true_range


@jit(nopython=True, cache=True)
def average_true_range(high, low, close, period=14):
    # Calculate the Average True Range using the true_range function
    true_ranges = true_range(high, low, close)
    atr = np.zeros_like(true_ranges)

    # Calculate the initial ATR as the average of the first "period" true ranges
    atr[period - 1] = np.mean(true_ranges[:period])

    # Calculate the subsequent ATR values using the following formula:
    # ATR[i] = (ATR[i-1] * (period - 1) + true_range[i]) / period
    for i in range(period, len(true_ranges)):
        atr[i] = (atr[i - 1] * (period - 1) + true_ranges[i]) / period

    return atr


# Example usage:
high_prices = np.array([100, 102, 105, 98, 110, 115, 108, 112, 120, 125])
low_prices = np.array([90, 92, 95, 88, 100, 105, 98, 102, 110, 115])
close_prices = np.array([95, 98, 101, 94, 105, 110, 103, 108, 115, 120])

print("starting")

atr_values = average_true_range(high_prices, low_prices, close_prices, period=4)
print(atr_values)


talib_atr = talib.ATR(high_prices, low_prices, close_prices, 4)
# print(talib_atr)
