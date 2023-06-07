from binance.client import Client
import pandas as pd
import mplfinance as mpf
from lib.create_binance_dataframe import create_binance_dataframe


def get_data(asset):
    print(f"Getting data for {asset}")
    client = Client()
    klines = client.get_historical_klines(
        asset,
        Client.KLINE_INTERVAL_1HOUR,
        "3000 day ago UTC",
    )

    df = create_binance_dataframe(klines)
    df.to_parquet(f"data/binance-{asset}-1h.parquet")
    df
    # mpf.plot(
    #     df,
    #     type="candle",
    #     volume=False,
    # )


from lib.multiprocess import multiprocess

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
]

multiprocess(assets, get_data)
