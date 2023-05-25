import mplfinance as mpf
import pandas as pd


def plot_ohlc(data, equity, entries, exits, ma_long, ma_short, rsi, atr):
    entry_data = pd.DataFrame(
        {"entry": data.close[entries], "value": 1}, index=entries.index
    )
    exit_data = pd.DataFrame({"exit": data.close[exits], "value": 1}, index=exits.index)

    mpf.plot(
        data,
        type="candle",
        volume=False,
        addplot=[
            mpf.make_addplot(ma_long, panel=0, color="blue"),
            mpf.make_addplot(ma_short, panel=0, color="orange"),
            mpf.make_addplot(atr, panel=0, color="black"),
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
