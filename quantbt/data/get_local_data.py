import os
from quantbt.lib import pd
from helpers.log import print
from quantbt.lib import find_files
from quantbt.lib.time_manip import time_manip
from quantbt.data.resample import resample

HOME = os.path.expanduser("~")

DATA_BASE = f"{HOME}/OHLC_data"

default_pair = {
    "base": "@ENQ/steps",
    "asset": "ENQ",
    "timeframe": "10",
}


def get_local_data(
    pair=default_pair,
    months_ago=None,
    hours_ago=None,
    days_ago=None,
    resample_tf=None,
):
    base = pair["base"]
    asset = pair["asset"]
    timeframe = pair["timeframe"]

    LOCATION = f"{DATA_BASE}/{base}"
    OFFSET = len(LOCATION.split("/"))

    assets = find_files(f"{LOCATION}", asset)
    for _asset in assets:
        if _asset.split("/")[OFFSET].split(".")[0] == f"{asset}-{timeframe}":
            data = pd.read_parquet(_asset)
            break

    ## Format Data
    data = time_manip.format_index(data)

    data.rename(
        {
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        },
        inplace=True,
        axis=1,
    )

    ## Filter Data
    if months_ago:
        data = time_manip.months_ago(data, months_ago)
    if hours_ago:
        data = time_manip.hours_ago(data, hours_ago)
    if days_ago:
        data = time_manip.hours_ago(data, 24 * days_ago)

    data.set_index("date", inplace=True)
    print("resampling")
    if resample_tf:
        data = resample(data, resample_tf)

    return data
