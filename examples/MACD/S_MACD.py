import quantbt as qnb
from quantbt.lib import find_files, optimize
import mplfinance as mpf
import pandas as pd

import talib
import numpy as np

SMA = qnb.indicators.SMA


class S_MACD(qnb.S_base):
    def get_signals(self, params):
        (
            atr_distance,
            sma,
            rsi,
            rsi_entry,
            rsi_exit,
            macd_fast,
            macd_slow,
            macd_signal,
        ) = params
        close = self.data.Close

        macd_line, macd_signal, macd_hist = talib.MACD(
            close, fastperiod=macd_fast, slowperiod=macd_slow, signalperiod=macd_signal
        )
        self.macd_line = macd_line
        self.macd_signal = macd_signal
        self.rsi = talib.RSI(close, timeperiod=rsi)
        self.sma = SMA(close, sma)

        self.entries = np.logical_and(
            np.logical_or(self.rsi <= rsi_entry, macd_line > macd_signal),
            close >= self.sma,
        )
        self.exits = self.rsi >= rsi_exit
        #
        self.sl = np.zeros_like(close)
        self.atr = talib.ATR(self.data.High, self.data.Low, close, 14)
        self.sl = self.data.Low - self.atr * atr_distance

    def plot_ohlc(self, offset=0):
        data = self.data[offset:]
        data.index = pd.to_datetime(data.index, unit="s")
        equity = self.equity[offset:]
        entries = self.entries[offset:]
        exits = self.exits[offset:]
        macd_line = self.macd_line[offset:]
        macd_signal = self.macd_signal[offset:]
        ma = self.sma[offset:]
        rsi = self.rsi[offset:]

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
                mpf.make_addplot(ma, panel=0, color="blue"),
                # mpf.make_addplot(atr, panel=0, color="black"),
                mpf.make_addplot(
                    entry_data["entry"],
                    type="scatter",
                    panel=0,
                    color="green",
                    markersize=50,
                ),
                mpf.make_addplot(
                    exit_data["exit"],
                    type="scatter",
                    panel=0,
                    color="red",
                    markersize=50,
                ),
                # mpf.make_addplot(
                #     exit_data["exit"], type="scatter", panel=0, color="red", markersize=50
                # ),
                # mpf.make_addplot(equity, panel=1),
                mpf.make_addplot(rsi, panel=1),
                mpf.make_addplot(macd_line, panel=2, color="black"),
                mpf.make_addplot(macd_signal, panel=2),
            ],
        )


assets = find_files("./data/", "binance")
assets


data = pd.read_parquet(assets[3])
data = data.resample("30min").last()
data
# data = data[-5000:]
# data = data[1:300]


def single(params, use_sl=True):
    bt = S_MACD(data, initial_capital=10000, use_sl=use_sl, commission=0.0006)
    bt.backtest(params)
    return bt


pf = single((20, 200, 14, 17, 99, 16, 26, 9))
print(pf.stats)
pf.data.index = pd.to_datetime(pf.data.index, unit="s")
pf.plot_equity()

# pf = single((10, 200, 14, 17, 99, 16, 26, 9), use_sl=False)
# print(pf.stats)
# pf.data.index = pd.to_datetime(pf.data.index, unit="s")

# |%%--%%| <YGn4XRP7u2|kvQLTwTn12>


prices = pd.Series(pf.equity, index=data.index)


# |%%--%%| <kvQLTwTn12|9CahcVLTTC>


optimisation = optimize(
    data,
    S_MACD,
    sma=range(100, 300, 1),
    rsi_low=range(5, 30, 1),
    rsi_high=range(70, 95, 1),
)
orignal = optimisation.copy()
optimisation = optimisation.sort_values("dd", ascending=False)
optimisation
# |%%--%%| <9CahcVLTTC|eepeiBiH4O>

optimisation = orignal.sort_values("ratio", ascending=True)
optimisation
