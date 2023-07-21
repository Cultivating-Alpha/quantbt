import pandas as pd
from optimisation_combine_files import combine_files
from strategies.S_rsi import S_rsi


# |%%--%%| <LPKGMSTXen|Zaep5G6FEi>


# df = combine_files("WETH-USDC")
# df = combine_files("WMATIC-USDC")

# |%%--%%| <Zaep5G6FEi|qqzgleyetT>


def process(df):
    df = df[df["ratio"] > 1]
    # df.sort_values("final_value", ascending=False, inplace=True)
    df.sort_values("ratio", ascending=False, inplace=True)
    # print(df.head(10))
    return df


matic = pd.read_parquet("./optimisation/WMATIC-USDC.full.parquet")
matic = process(matic)
matic

eth = pd.read_parquet("./optimisation/WETH-USDC.full.parquet")
eth = process(eth)
eth

# Define the subset of columns to consider
subset_columns = ["long", "short", "rsi", "atr"]

# Find the common rows based on the subset of columns
common_rows = pd.merge(matic, eth, on=subset_columns)
common_rows["ratio"] = common_rows.apply(
    lambda row: max(row["ratio_x"], row["ratio_y"]), axis=1
)
common_rows = process(common_rows)

common_rows = common_rows.sort_values(by=["ratio_x", "ratio_y"], ascending=False)
common_rows.drop(
    [
        "dd_y",
        "final_value_y",
        "total_return_y",
        "total_return_x",
        "final_value_x",
        "dd_x",
    ],
    inplace=True,
    axis=1,
)
common_rows.head(10)

# |%%--%%| <qqzgleyetT|eExQjYTN4d>


asset = "./data/uniswap_v3-ethereum-WETH-USDC-4h.parquet"
bt_eth = S_rsi(asset)
bt_eth.backtest((295, 11, 9, 2.5))
print(bt_eth.stats)


asset = "./data/uniswap_v3-polygon-WMATIC-USDC-4h.parquet"
bt_matic = S_rsi(asset)
bt_matic.backtest((295, 11, 9, 2.5))
bt_matic.stats
