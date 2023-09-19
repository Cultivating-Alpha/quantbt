import pandas as pd


class Monthly:
    def __init__(self, INITIAL_CAPITAL):
        self.monthly = None
        self.INITIAL_CAPITAL = INITIAL_CAPITAL

    def backtest_each_month(self, strategy, **backtest_vars):
        df = strategy.st.original_data.copy()
        df["date"] = df.index
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
