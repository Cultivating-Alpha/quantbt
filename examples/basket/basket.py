import numpy as np
import pandas as pd
import mplfinance as mpf
from quantnb.core.backtester import Backtester
from quantnb.lib import find_files, plotting
from quantnb.indicators import supertrend, SMA, cross_below, cross_above

assets = find_files("./data", "binance")

datas = {}
for asset in assets:
    datas[asset.split("-")[1]] = pd.read_parquet(asset)


# |%%--%%| <h1NJ8eCQd7|s4tvHELefh>

data = datas["BTCUSDT"]
data = data[0:300]


class S_basket:
    def __init__(self, data) -> None:
        self.data = data
        self.generate_signals()

    def generate_signals(self):
        df = self.data
        supert = supertrend(
            df.high.values,
            df.low.values,
            df.close.values,
            period=10,
            multiplier=3,
        )[0]
        sma = SMA(df.close.values, period=100)

        self.supert = supert
        self.sma = sma

        self.entry = np.logical_and(
            cross_above(data.close.values, supert), data.close > sma
        )
        self.exit = cross_below(data.close.values, supert)

    def backtest(self):
        bt = Backtester(self.data)
        bt.backtest(self.entry, self.exit)

    def plot(self):
        plotting.mpf_plot(
            self.data,
            [
                plotting.add_line_plot(self.supert, color="teal"),
                plotting.add_line_plot(self.sma, color="blue"),
                plotting.add_markers(self.entry, data, color="green"),
                plotting.add_markers(self.exit, data, color="red"),
            ],
        )


bt = S_basket(data)
bt.plot()
