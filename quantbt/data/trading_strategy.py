import pandas as pd
import requests
import json


def get_trading_strategy_data(pair_id, exchange_type, time_bucket, start, old_df=None):
    url = f"https://tradingstrategy.ai/api/candles?pair_id={pair_id}&exchange_type={exchange_type}&time_bucket={time_bucket}&start={start}"

    # Perform the request
    response = requests.get(url)
    data = json.loads(response.text)
    data = data[str(pair_id)]
    _df = pd.read_json(json.dumps(data))

    # Read the JSON data from the URL into a DataFrame

    if old_df is None:
        old_df = pd.DataFrame()
    df = pd.DataFrame()
    df["open"] = _df["o"]
    df["high"] = _df["h"]
    df["low"] = _df["l"]
    df["close"] = _df["c"]
    df["volume"] = _df["v"]
    df["date"] = _df["ts"]

    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%dT%H:%M:%S")
    df.set_index("date", inplace=True)

    df = pd.concat([old_df, df])

    now = pd.Timestamp.now()
    end_date = df.index[-1]
    diff = now - end_date

    if diff.days > 0:
        print("getting more")
        print(end_date.strftime("%Y-%m-%d"))
        return get_trading_strategy_data(
            pair_id, exchange_type, time_bucket, end_date.strftime("%Y-%m-%d"), df
        )
    else:
        df = df[~df.index.duplicated(keep="first")]
        return df
