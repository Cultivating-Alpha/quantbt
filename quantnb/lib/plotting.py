import pandas as pd
from .time_manip import TimeManip
import matplotlib.pyplot as plt
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

    def add_markers(self, markers, data, panel=0, color="black"):
        markers = convert_signal_to_marker(markers, data.Close, data.index)
        return mpf.make_addplot(
            markers,
            type="scatter",
            panel=panel,
            color=color,
            markersize=50,
        )

    def mpf_plot(self, data, subplots):
        # # Create my own `marketcolors` to use with the `nightclouds` style:
        # mc = mpf.make_marketcolors(up="white", down="red", inherit=True)
        #
        # # Create a new style based on `nightclouds` but with my own `marketcolors`:
        # s = mpf.make_mpf_style(base_mpf_style="nightclouds", marketcolors=mc)
        # Create MPF plot
        mpf.plot(
            data,
            type="candle",
            volume=False,
            ylabel="Price",
            addplot=subplots,
            style="classic",
            title="Strategy Oupput",
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

    def plot_equity(self, equity, data, bid_column):
        df = pd.DataFrame(
            {
                "equity": equity,
                "date": TimeManip().convert_ms_to_datetime(data["Date"].values),
                "Bid": data[bid_column].values,
            }
        )
        # print(df)

        df["bnh"] = df["Bid"].diff().cumsum() + 10000

        plt.plot(df["date"], df["equity"], label="Equity")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title("Two Lines Plot")
        plt.legend()
        plt.show()

        # x = df["date"]
        # y1 = df["equity"]
        # y2 = df["bnh"]
        #
        # # Create the figure and the first Y-axis
        # fig, ax1 = plt.subplots()
        #
        # # Plot the first line
        # ax1.plot(x, y1, "black", label="Strategy")
        # ax1.set_xlabel("X-axis")
        # ax1.set_ylabel("Line 1 Y-axis", color="b")
        # ax1.tick_params("y", colors="b")
        #
        # # Create the second Y-axis
        # ax2 = ax1.twinx()
        #
        # # Plot the second line
        # ax2.plot(x, y2, "gray", label="BnH")
        # ax2.set_ylabel("Line 2 Y-axis", color="r")
        # ax2.tick_params("y", colors="gray")
        #
        # # Add a legend
        # lines = [ax2.get_lines()[0], ax1.get_lines()[0]]
        # plt.legend(lines, [line.get_label() for line in lines])
        #
        # # Display the plot
        # plt.title("Two Lines with Separate Y-Axes")
        # plt.show()
        # return df


plotting = Plotting()
