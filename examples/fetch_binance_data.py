from quantbt.lib.fetch_binance_data import fetch_binance_data
from binance.client import Client
import pandas as pd



assets = [
    "ETHUSDT",
    # "BTCUSDT",
    # "DOGEUSDT",
    # "BNBUSDT",
    # "ATOMUSDT",
    # "NEOUSDT",
    # "NEOUSDT",
    # "XRPUSDT",
    # "LTCUSDT",
    # "TRXUSDT",
    # "AVAXUSDT",
    # "SHIBUSDT",
    # "ATOMUSDT",
    # "LINKUSDT",
    # "UNIUSDT",
    # "ADAUSDT",
    # "DOTUSDT",
    # "SOLUSDT",
    # "MATICUSDT",
    # "XLMUSDT",
]

fetch_binance_data(
        assets=assets, 
        tf=Client.KLINE_INTERVAL_5MINUTE, 
        days="3 day ago UTC",
        save_location="data")

df = pd.read_parquet("data/binance-ETHUSDT-5m.parquet")
print(df)


#|%%--%%| <EC3imhK9Jp|xeubjc1Zyx>


df['open'].plot()
plt.show()

