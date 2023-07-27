from quantnb.indicators.supertrend import supertrend
from quantnb.indicators.SMA import SMA
from quantnb.indicators.random_data import random_data
import mplfinance as mpf
import random
import pandas as pd
import numpy as np

# np.random.seed(12)

open, high, low, close, ohlc_data = random_data()


supert, superd, superl, supers = supertrend(
    high,
    low,
    close,
    period=10,
    multiplier=3,
)


# Create MPF plot
mpf.plot(
    ohlc_data,
    type="candle",
    volume=False,
    ylabel="Price",
    addplot=[
        mpf.make_addplot(supert, color="red", panel=0),
        # mpf.make_addplot(supers, color="red", panel=0),
        # mpf.make_addplot(superl, color="teal", panel=0),
    ],
    title="Supertrend Indicator",
)
