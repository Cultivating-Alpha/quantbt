from quantnb.lib.fetch_binance_data import fetch_binance_data


fetch_binance_data()

# |%%--%%| <N7dBWmxr3c|NImzBBNtIq>

import pandas as pd

df = pd.read_parquet("data/binance-XLMUSDT-1h.parquet")
df
