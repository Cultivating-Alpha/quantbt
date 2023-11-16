import pandas as pd
from .time_manip import TimeManip
import matplotlib.pyplot as plt
import matplotlib
import mplfinance as mpf
from .convert_signal_to_markers import convert_signal_to_marker


class Plotting:
    def __init__(self):
        pass

    # ================================================================================= #
    #                             SubPlotting Methods                                   #
    # ================================================================================= #
    def add_line_plot(self, data, panel=0, color="black"):
        return mpf.make_addplot(data, color=color, panel=panel)

    def add_markers(
        self,
        markers,
        data,
        panel=0,
        color="black",
        marker_type=matplotlib.markers.CARETDOWN,
    ):
        markers = convert_signal_to_marker(markers, data, data.index)
        return mpf.make_addplot(
            markers,
            type="scatter",
            marker=marker_type,
            panel=panel,
            color=color,
            markersize=50,
        )

    def mpf_plot(self, data, subplots=[], type="candle"):
        # # Create my own `marketcolors` to use with the `nightclouds` style:
        # mc = mpf.make_marketcolors(up="white", down="red", inherit=True)
        #
        # # Create a new style based on `nightclouds` but with my own `marketcolors`:
        # s = mpf.make_mpf_style(base_mpf_style="nightclouds", marketcolors=mc)
        # Create MPF plot
        mpf.plot(
            data,
            type=type,
            volume=False,
            ylabel="Price",
            addplot=subplots,
            title="Strategy Output",
        )

    # ================================================================================= #
    #                              Plotting Methods                                     #
    # ================================================================================= #
    def plot_orders(self, time, price, direction, is_time_ms=False):
        if is_time_ms:
            time = pd.to_datetime(time, unit="ms")
        # Extract relevant data from 'orders' array or DataFrame
        x = time
        y = price
        colors = direction

        # Create a scatter plot
        plt.scatter(x, y, c=colors)

        # Set labels and display the plot
        plt.xlabel("Open Time")
        plt.ylabel("Open Price")
        plt.title("Scatter Plot of Orders")
        plt.show()

    def plot_trades(self, open_time, close_time, open_price, close_price):
        x = [open_time, close_time]
        y = [open_price, close_price]

        # Plot the line
        plt.plot(x, y)

        # Set labels and display the plot
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.title("Lines between Points")
        plt.show()

    def plot_volumes(self, time, volume, is_time_ms=False):
        if is_time_ms:
            time = pd.to_datetime(time, unit="ms")
        # Plot the scatter
        plt.plot(time, volume)

        # Set labels and display the plot
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.title("Lines between Points")
        plt.show()

    def plot_equity(self, bt, data, bid_column="Close"):
        equity = bt.data_module.equity
        df = pd.DataFrame(
            {
                "equity": equity,
                "Date": TimeManip().convert_s_to_datetime(data.index.values),
                "Bid": data[bid_column].values,
            }
        )

        # df["bnh"] = df["Bid"].diff().cumsum() + 10000
        df["Open"] = df["equity"]
        df["High"] = df["equity"]
        df["Low"] = df["equity"]
        df["Close"] = df["equity"]
        df.set_index("Date", inplace=True)

        # subplots = self.add_line_plot(df["bnh"], panel=0, color="black")
        subplots = []

        self.mpf_plot(df, subplots=subplots, type="line")
        return df


plotting = Plotting()
