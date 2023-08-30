from .S_base import S_base
from ..indicators import SMA
import mplfinance as mpf
import pandas as pd

import talib
import numpy as np


class S_Test(S_base):
    def get_signals(self, params):
        long, short, cutoff, atr_distance = params
        close = self.data.Close
        self.ma_long = SMA(close, long)
        self.ma_short = SMA(close, short)
        self.rsi = talib.RSI(close, timeperiod=2)
        self.atr = talib.ATR(self.data.High, self.data.Low, close, 14)

        self.entries = np.logical_and(
            close <= self.ma_short,
            np.logical_and(close >= self.ma_long, self.rsi <= cutoff),
        )
        self.exits = close > self.ma_short

        self.sl = self.data.Low - self.atr * atr_distance

    def plot_ohlc(self, offset=0):
        data = self.data[offset:]
        data.index = pd.to_datetime(data.index, unit="s")
        equity = self.equity[offset:]
        entries = self.entries[offset:]
        exits = self.exits[offset:]
        ma_long = self.ma_long[offset:]
        ma_short = self.ma_short[offset:]
        rsi = self.rsi[offset:]
        sl = self.sl[offset:]

        entries.index = data.index
        exits.index = data.index

        entry_data = pd.DataFrame(
            {"entry": data.Close[entries], "value": 1}, index=entries.index
        )
        exit_data = pd.DataFrame(
            {"exit": data.Close[exits], "value": 1}, index=exits.index
        )

        mpf.plot(
            data,
            type="candle",
            volume=False,
            addplot=[
                mpf.make_addplot(ma_long, panel=0, color="blue"),
                mpf.make_addplot(ma_short, panel=0, color="orange"),
                # mpf.make_addplot(atr, panel=0, color="black"),
                mpf.make_addplot(
                    entry_data["entry"],
                    type="scatter",
                    panel=0,
                    color="green",
                    markersize=50,
                ),
                # mpf.make_addplot(
                #     exit_data["exit"], type="scatter", panel=0, color="red", markersize=50
                # ),
                mpf.make_addplot(equity, panel=1),
                mpf.make_addplot(rsi, panel=2),
            ],
        )
