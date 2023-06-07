from strategies.S_rsi import S_rsi
import pandas as pd


bt = S_rsi("./data/uniswap_v3-ethereum-WETH-USDC-4h.parquet")
# bt.backtest((200, 10, 10, 1))
bt.backtest((200, 11, 9, 2.5))

bt2 = S_rsi("./data/uniswap_v3-ethereum-WMATIC-USDC-4h.parquet")
# bt2.backtest((200, 10, 10, 1))
bt2.backtest((200, 11, 9, 2.5))


# final_equity = bt.equity + bt2.equity

df = pd.DataFrame(
    {
        "pair": ["WETH-USDC", "WMATIC-USDC"],
        "dd": ["-32.2%", "-12%"],
        "total_return": ["-14%", "110%"],
    }
)
df2 = pd.DataFrame(
    {
        "pair": ["WETH-USDC", "WMATIC-USDC"],
        "dd": ["-23.5.2%", "-22%"],
        "total_return": ["66%", "42%"],
    }
)
print()
print()
print(df)
print()
print()
print(df2)
# df2
