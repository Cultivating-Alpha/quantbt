"""
Given a seed, generate random candlesticks data
"""
# from quantnb.indicators.supertrend import supertrend
# from quantnb.indicators.SMA import SMA
# import mplfinance as mpf
# import random
import pandas as pd
import numpy as np


def random_data(seed=None):
    if seed:
        np.random.seed(seed)

    # Define parameters
    num_periods = 1000
    initial_price = 100.0
    volatility = 0.02  # Daily volatility (standard deviation)
    drift = 0.0  # Average daily return

    # Generate random price returns
    returns = np.random.normal(loc=drift, scale=volatility, size=num_periods - 1)
    prices = initial_price * (1 + np.cumsum(returns))

    # Generate random OHLC data
    open_prices = prices[:-1]
    random_shift = np.random.uniform(low=0, high=2, size=len(open_prices))
    high_prices = np.maximum(open_prices, prices[1:]) + random_shift
    low_prices = np.minimum(open_prices, prices[1:]) - random_shift
    close_prices = prices[1:]

    # Create DataFrame
    dates = pd.date_range(start="2023-01-01", periods=num_periods, freq="D")
    ohlc_data = pd.DataFrame(
        {
            "date": dates[:-2],
            "open": open_prices,
            "high": high_prices,
            "low": low_prices,
            "close": close_prices,
        }
    )
    ohlc_data.set_index("date", inplace=True)
    return (
        ohlc_data["open"].values,
        ohlc_data["high"].values,
        ohlc_data["low"].values,
        ohlc_data["close"].values,
        ohlc_data,
    )
