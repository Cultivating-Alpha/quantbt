from .S_base import S_base
import mplfinance as mpf
import pandas as pd


class S_bid_ask(S_base):
    def set_signals(self, long_entries, long_exits):
        self.entries = long_entries
        self.exits = long_exits

    def get_signals(self, params):
        pass

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
