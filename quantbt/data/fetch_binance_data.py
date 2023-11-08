import pandas as pd
import mplfinance as mpf
from ..lib import time_manip
from datetime import datetime
from binance.client import Client
from .create_binance_dataframe import create_binance_dataframe


def get_data(
    asset, tf=Client.KLINE_INTERVAL_1HOUR, days="3000 day ago UTC", save_location="data"
):
    # asset = asset[0]
    print(f"Getting data for {asset} on {tf}")
    client = Client()
    klines = client.get_historical_klines(asset, tf, days)

    df = create_binance_dataframe(klines)
    df.to_parquet(f"{save_location}/binance-{asset}-{tf}.parquet")


def fetch_binance_data(
    assets=None,
    tf=Client.KLINE_INTERVAL_5MINUTE,
    days="3 day ago UTC",
    save_location="data",
):
    if assets is None:
        print("Please provide at least one asset item")
    else:
        for asset in assets:
            get_data(asset, tf, days, save_location)


def fetch_futures_data(
    symbol="BTCUSDT", count=30, tf="1m", contract_type="PERPETUAL", limit=1500
):
    fetcher = FuturesFetcher()

    # Fetch PERPETUAL CONTRACTS
    df = fetcher.fetch(symbol, count, tf, contract_type, limit)
    df.to_parquet(f"./data/binance-{symbol}-{contract_type}-{tf}.parquet")
    print(df)


class FuturesFetcher:
    def __init__(self):
        self.client = Client()
        pass

    def _fetch(self, symbol, end, tf="1m", contract_type="PERPETUAL", limit=1500):
        print(end)
        r = self.client.futures_continous_klines(
            pair=symbol,
            contractType=contract_type,
            interval=tf,
            limit=limit,
            endTime=int(end.timestamp() * 1000),
        )
        df = pd.DataFrame(r)

        df.columns = [
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "number_of_trades",
            "taker_buy_volume",
            "taker_buy_quote_asset_volume",
            "ignore",
        ]
        df["time"] = time_manip.convert_ms_to_datetime(df["time"])
        df.set_index("time", inplace=True)
        return df

    def fetch(self, symbol, count, tf, contract_type, limit):
        df = self._fetch(symbol, datetime.now(), tf, contract_type, limit)
        for i in range(count):
            newdf = self._fetch(symbol, df.index[0], tf, contract_type, limit)
            df = pd.concat([newdf, df])
        return df
