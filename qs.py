# df = pd.DataFrame(bt_matic.equity, index=bt_matic.data.index)
# df.resample("1M").last()
# plt.bar(df.index, df[0])
import quantstats as qs
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


import matplotlib.colors as mcolors


qs.extend_pandas()


def report(bt):
    data = bt.data.copy()
    equity = bt.equity

    qs.extend_pandas()
    annual_rf_rate = 0.05
    rf_rate = (1 + annual_rf_rate) ** (1 / (252 * 60)) - 1
    # show sharpe ratio
    prices = data.Close
    data.reset_index(inplace=True)
    eq = pd.Series(equity, index=data["Date"])
    eq.plot()
    returns = pd.Series(equity, index=data["Date"])

    monthly_returns = returns.resample("M").ffill().pct_change()
    print(monthly_returns)

    # Convert the series to a dataframe with a single column
    monthly_returns_df = pd.DataFrame({"Returns": monthly_returns})

    # Extract the year and month from the index
    monthly_returns_df["Year"] = monthly_returns_df.index.year
    monthly_returns_df["Month"] = monthly_returns_df.index.month

    # Pivot the data to create a grid of monthly returns
    monthly_returns_grid = monthly_returns_df.pivot(
        index="Year", columns="Month", values="Returns"
    )

    sns.set(font_scale=0.3)
    # Create a custom color palette from light orange to green
    # Define custom color values for the colormap
    color_list = ["#C2DFFF", "#006400"]  # Light blue to dark green

    # Create a custom colormap using LinearSegmentedColormap
    seagreen_cmap = mcolors.LinearSegmentedColormap.from_list("seagreen", color_list)

    # Create a heatmap of monthly returns
    plt.figure(figsize=(10, 6))
    sns.heatmap(monthly_returns_grid, cmap=seagreen_cmap, annot=True, fmt=".2%")
    plt.xlabel("Month")
    plt.ylabel("Year")
    plt.title("Heatmap of Monthly Returns")
    plt.show()


# report(bt_matic)
# report(bt_eth)


df1 = pd.Series(bt_matic.equity, index=bt_matic.data.index)
df2 = pd.Series(bt_eth.equity, index=bt_eth.data.index)
df1 = df1.reindex(df2.index)
df1.plot()
df2.plot()
plt.show()
