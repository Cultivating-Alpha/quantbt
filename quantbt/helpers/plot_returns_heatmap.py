import quantstats as qs
import seaborn as sns
import matplotlib.pyplot as plt
from quantbt.lib import pd, np


def plot_returns_heatmap(df, bound=None):
    pct_change = df.pct_change()
    returns = qs.stats.monthly_returns(pct_change)
    returns = np.round(returns * 100, 2)
    print(returns)

    data = returns.iloc[:, :-1]
    data = data[data != 0]

    plot_heatmap(returns, bound)
    return returns


def plot_heatmap(df, bound=None):
    # bound = max(abs(data.min().min()), abs(data.max().max()))
    if bound == None:
        mean = df.mean().mean()
        bound = (mean * -1, mean)

    sns.heatmap(
        df,
        # cmap=GnRd,
        cmap="RdYlGn",
        fmt=".1f",
        cbar=True,
        annot=True,
        annot_kws={"size": 20},  # Adjust the font size for annotations
        linewidths=5,  # Add lines between cells for better separation
        square=True,  # Make cells square to ensure all values are visible
        vmin=bound[0],
        vmax=bound[1],
    )
    plt.show()


def create_pivot_df(df, index_name="name", column_name="diff"):
    df_resampled = df.resample("M").sum()

    # Reset the index to have years and months as separate columns
    df_resampled.reset_index(inplace=True)

    # Extract the year and month into separate columns
    df_resampled["Year"] = df_resampled[index_name].dt.year
    df_resampled["Month"] = df_resampled[index_name].dt.month

    # Pivot the DataFrame to have rows as years and columns as months
    pivot_df = df_resampled.pivot(index="Year", columns="Month", values=column_name)

    # Rename the columns to represent month names
    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    pivot_df.columns = [month_names[month - 1] for month in pivot_df.columns]
    print()
    # Fill NaN values with zeros if needed
    pivot_df = pivot_df.fillna(0)
    return pivot_df
