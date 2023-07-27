from binance.client import Client
import pandas as pd
import mplfinance as mpf
from .multiprocess import multiprocess
from .create_binance_dataframe import create_binance_dataframe


def get_data(asset, tf=Client.KLINE_INTERVAL_1HOUR, days="3000 day ago UTC"):
    # asset = asset[0]
    print(f"Getting data for {asset} on {tf}")
    client = Client()
    klines = client.get_historical_klines(asset, tf, days)

    df = create_binance_dataframe(klines)
    df.to_parquet(f"data/binance-{asset}-{tf}.parquet")


assets = [
    "BTCUSDT",
    "ETHUSDT",
    "DOGEUSDT",
    "BNBUSDT",
    "ATOMUSDT",
    "NEOUSDT",
    "NEOUSDT",
    "XRPUSDT",
    "LTCUSDT",
    "TRXUSDT",
    "AVAXUSDT",
    "SHIBUSDT",
    "ATOMUSDT",
    "LINKUSDT",
    "UNIUSDT",
    "ADAUSDT",
    "DOTUSDT",
    "SOLUSDT",
    "MATICUSDT",
    "XLMUSDT",
]


def fetch_binance_data(
    assets=assets, tf=Client.KLINE_INTERVAL_1HOUR, days="3000 day ago UTC"
):
    # multiprocess(assets, get_data, tf, days)
    for asset in assets:
        get_data(asset, tf, days)
