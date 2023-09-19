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

    # bound = max(abs(data.min().min()), abs(data.max().max()))
    if bound == None:
        mean = data.mean().mean()
        bound = (mean * -1, mean)

    sns.heatmap(
        returns,
        # cmap=GnRd,
        cmap="RdYlGn",
        fmt=".1f",
        cbar=True,
        annot_kws={"size": 4},  # Adjust the font size for annotations
        linewidths=5,  # Add lines between cells for better separation
        square=True,  # Make cells square to ensure all values are visible
        vmin=bound[0],
        vmax=bound[1],
    )
    plt.show()
    return returns
