import pandas as pd


def calculate_average_freq(data):
    df = pd.DataFrame()
    key = list(data.keys())[0]
    df["date"] = data[key].index
    avg = df["date"].agg(
        {
            "count": "count",
            "avg_time_diff": lambda group: group.sort_values().diff().mean(),
        }
    )
    return avg["avg_time_diff"].total_seconds() / 60 * pd.Timedelta(1, "m")
