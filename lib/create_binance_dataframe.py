import pandas as pd


def create_binance_dataframe(klines):
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
