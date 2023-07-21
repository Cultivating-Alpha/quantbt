import pandas as pd
import matplotlib.pyplot as plt


class Helper:
    def __init__(self):
        pass

    # ================================================================================= #
    #                        Time Manipulation Methods                                  #
    # ================================================================================= #
    def convert_ms_to_datetime(self, df):
        return pd.to_datetime(df, unit="ms")

    def convert_s_to_datetime(self, df):
        return pd.to_datetime(df, unit="s")

    def convert_datetime_to_s(self, df):
        return pd.to_datetime(df).astype(int) // 10**9

    def convert_datetime_to_ms(self, df):
        return pd.to_datetime(df).astype(int) // 10**6

    def convert_duration_to_timestamp(self, df, unit="ms"):
        return pd.to_timedelta(df, unit=unit)

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

    def plot_equity(self, equity, data):
        df = pd.DataFrame(
            {
                "equity": equity,
                "date": self.convert_ms_to_datetime(data["Date"].values),
                "Bid": data["Bid"].values,
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
