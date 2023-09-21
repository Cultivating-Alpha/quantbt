import pandas as pd
from quantbt.helpers import plot_heatmap, create_pivot_df, plot_barchart


class Monthly:
    def __init__(self, INITIAL_CAPITAL):
        self.monthly = None
        self.INITIAL_CAPITAL = INITIAL_CAPITAL

    def backtest_each_month(self, strategy, **backtest_vars):
        df = strategy.st.data.copy()
        # df["date"] = df.index
        grouped = df.groupby(pd.Grouper(key="date", freq="M"))

        stats = pd.DataFrame()
        equities = {}
        for name, group in grouped:
            # plotting.mpf_plot(group)
            strategy.st.set_data(group)
            new_stats = strategy.backtest(**backtest_vars)
            new_stats["name"] = name
            new_stats.set_index("name", inplace=True)
            stats = pd.concat([stats, new_stats])
            # print()
            # print(f"=== {name}")
            # print(new_stats)

            new_equity = strategy.st.bt.data_module.equity
            equities[name] = new_equity
        self.monthly = stats
        self.equities = equities

        self.calculate_summary()
        self.calculate_cumsum()
        return stats

    def calculate_summary(self):
        if self.monthly is not None:
            monthly = self.monthly
            df = monthly.copy()
            min_values = df.min()
            max_values = df.max()
            mean_values = df.mean()
            summary_data = {"min": min_values, "mean": mean_values, "max": max_values}
            summary_df = pd.DataFrame(summary_data).transpose()
            self.summary = summary_df
            return summary_df

    def calculate_cumsum(self):
        if self.monthly is not None:
            monthly = self.monthly
            monthly["diff"] = monthly["End Value"] - self.INITIAL_CAPITAL
            df = monthly["diff"]
            df[0] += self.INITIAL_CAPITAL
            df = df.cumsum()
            self.cumsum = df
            return df

    # ================================================================================================= #
    #                                         PLOTTING FUNCTIONS                                        #
    # ================================================================================================= #
    def get_monthly_returns(self):
        df = pd.DataFrame(
            {"diff": self.monthly["End Value"] - self.INITIAL_CAPITAL},
            index=self.monthly.index,
        )
        df["diff"] = df["diff"] * 100 / self.INITIAL_CAPITAL
        return df

    def draw_monthly_returns_bar(self, color="teal"):
        df = self.get_monthly_returns()
        plot_barchart(df.index, df["diff"].values, color)
        return df

    def draw_monthly_returns_heatmap(self):
        df = self.get_monthly_returns()
        pivot_df = create_pivot_df(df)
        plot_heatmap(pivot_df)
        print(pivot_df)

    def draw_monthly_dd_heatmap(self):
        df = pd.DataFrame(
            {"diff": self.monthly["DD"] * -1},
            index=self.monthly.index,
        )
        pivot_df = create_pivot_df(df)
        plot_heatmap(pivot_df)
        print(pivot_df)
