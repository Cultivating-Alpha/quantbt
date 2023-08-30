from binance.client import Client
import pandas as pd
import mplfinance as mpf
from quantnb.lib.create_binance_dataframe import create_binance_dataframe


def get_data(asset, tf=Client.KLINE_INTERVAL_1HOUR, days="3000 day ago UTC", save_location="data"):
    # asset = asset[0]
    print(f"Getting data for {asset} on {tf}")
    client = Client()
    klines = client.get_historical_klines(asset, tf, days)

    df = create_binance_dataframe(klines)
    df.to_parquet(f"{save_location}/binance-{asset}-{tf}.parquet")




def fetch_binance_data(
    assets=None, tf=Client.KLINE_INTERVAL_5MINUTE, days="3 day ago UTC", save_location="data"
):
    if assets is None:
        print("Please provide at least one asset item")
    else:
        for asset in assets:
            get_data(asset, tf, days, save_location)

