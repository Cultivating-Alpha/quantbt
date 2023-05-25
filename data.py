from binance.client import Client
import pandas as pd
import mplfinance as mpf


def binanceDataFrame(klines):
    df = pd.DataFrame(
        klines,
        dtype=float,
        columns=(
            "Open Time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            "Close time",
            "Quote asset volume",
            "Number of trades",
            "Taker buy base asset volume",
            "Taker buy quote asset volume",
            "Ignore",
        ),
    )

    df["Open Time"] = pd.to_datetime(df["Open Time"], unit="ms")
    df.drop(
        columns=[
            "Close time",
            "Quote asset volume",
            "Number of trades",
            "Taker buy base asset volume",
            "Taker buy quote asset volume",
            "Ignore",
        ],
        inplace=True,
    )
    # Rename columns using a dictionary
    new_column_names = {
        "Open Time": "Date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume",
    }
    df = df.rename(columns=new_column_names)
    df.set_index("Date", inplace=True)

    return df


client = Client()
klines = client.get_historical_klines(
    # klines = client.get_futures_historical_klines(
    "ETHUSDT",
    Client.KLINE_INTERVAL_4HOUR,
    "3000 day ago UTC",
)

df = binanceDataFrame(klines)
df.to_parquet("data/binance-ETHUSDT.parquet")
df
# mpf.plot(
#     df,
#     type="candle",
#     volume=False,
# )
