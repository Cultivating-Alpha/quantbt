import pandas as pd
import numpy as np

# from helpers.calculate_risk_free import calculate_risk_free
# from helpers.save_to_csv import save_to_csv
import matplotlib.style as style
import matplotlib.pyplot as plt

import mplfinance as mpf


class Helpers:
    def old_save_to_csv(self, pf, data, signal, indicators, data_item_index=0):
        key = list(data.data.keys())[data_item_index]

        df = data.data[key].copy()
        df = pd.DataFrame(
            {
                "open": df.Open,
                "high": df.High,
                "low": df.Low,
                "close": df.Close,
            }
        )
        df.reset_index(inplace=True)
        df.rename(columns={"Open time": "Date"}, inplace=True)
        df.set_index("Date", inplace=True)

        if hasattr(signal, "columns"):
            indicators = [indicators.iloc[:, data_item_index]]
            indicators = [indicators]
            signal = signal.iloc[:, data_item_index]
            # pf = pf.loc[:, pf.wrapper.columns[data_item_index]]
        else:
            indicators = indicators

        save_to_csv(pf, df, signal, indicators, "")

    def save_to_csv(data, i, i2, signal, equity, strategy, name="TEST"):
        df = data.copy()
        df["i"] = i
        df["i2"] = i2
        df["dd"] = signal

        df["e"] = equity
        # short_orders = np.full_like(pf.orders.mask, 0, dtype=float)
        # long_orders = np.full_like(pf.orders.mask, 0, dtype=float)
        #
        # for order in pf.orders.records_arr:
        #     row = order[3]
        #     if order[8] == 1:
        #         short_orders[row] = order[6]
        #     else:
        #         long_orders[row] = order[6]
        # df["short_order"] = short_orders
        # df["long_order"] = long_orders
        print(df[200:])
        df[200:].to_csv(f"/home/alpha/workspace/cultivating-alpha/UI/public/TEST.csv")

    def print_trades(self, pf):
        if hasattr(pf.trades.mask, "columns"):
            df = pf.trades.loc[:, pf.trades.mask.columns[0]].records_readable
        else:
            df = pf.trades.records_readable
        df = df.sort_values(by="Entry Index")
        df = df.reset_index()
        df.drop(
            columns=[
                # "Size",
                "index",
                "Position Id",
                "Status",
                # "Entry Fees",
                # "Exit Fees",
                "Return",
                "Exit Order Id",
                "Exit Trade Id",
                "Column",
                "Entry Order Id",
            ],
            inplace=True,
        )
        df.set_index("Entry Index", inplace=True)
        df.to_csv("trades.csv")
        return df

    def trades_per_day(self, pf):
        stats = pf.stats()
        trades_per_day = stats["Total Trades"] / stats["Period"].days
        print(trades_per_day)

    def pf_stats(self, pf, data):
        print(pf.stats(settings=dict(risk_free=calculate_risk_free(data))))

    def plot_as_ohlc(self, pf, aggregation="D"):
        df = pf.get_value().copy()
        df = df.dropna()

        # # calculate the monthly returns
        aggregated = df.resample(aggregation).ohlc()

        mpf.plot(aggregated, type="candle")

    def plot(self, pf, aggregation="D"):
        df = pf.get_value().copy()
        # df = df.dropna()

        # # calculate the monthly returns
        aggregated = df.resample(aggregation).last()
        #
        # # df = pd.read_hdf("pf.h5", key="pf")
        # df = df.astype(int)
        #
        # # # plot the equity as a line graph
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(aggregated.index, aggregated)
        # ax.plot(monthly_returns.index, monthly_returns)
        ax.set_title("Equity Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Equity")
        plt.show()

    def plot_returns(self, pf, aggregation="M"):
        df = pf.get_value().copy()
        df = df.dropna()
        # # calculate the monthly returns
        monthly_returns = df.resample(aggregation).last()
        monthly_returns

        monthly_diff = monthly_returns.diff()
        monthly_diff

        # plot the histogram of the difference with small width
        s = monthly_diff
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(
            np.arange(len(s)),
            bins=len(s),
            range=(0, len(s)),
            width=0.8,
            weights=monthly_diff,
        )
        ax.set_title("Histogram of Monthly Difference")
        ax.set_xlabel("Index")
        ax.set_ylabel("Difference")
        ax.set_xticks(np.arange(len(s)))
        ax.set_xticklabels(s.index.strftime("%b %Y"), rotation=45, ha="right")
        plt.show()
