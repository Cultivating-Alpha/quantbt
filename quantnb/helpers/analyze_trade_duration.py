from datetime import timedelta


def analyze_trade_duration(pf):
    df = pf.trades.records_readable
    entries = df["Entry Index"]
    exists = df["Exit Index"]
    diff = exists - entries
    df["diff"] = diff < timedelta(minutes=1)

    df = pf.trades.records_readable
    entries = df["Entry Index"]
    exists = df["Exit Index"]
    diff = exists - entries
    df["diff"] = diff > timedelta(minutes=1)
    df = df[df["diff"] == True]
    # print(
    #     "ANalyzing the trades that last more than 1 min: ", len(df), len(df) / 165
    # )

    df = pf.trades.records_readable
    df["diff"] = diff < timedelta(minutes=1)
    df = df[df["diff"] == True]
    # print("ANalyzing the trades that last less than 1 min", len(df), len(df) / 165)
    return len(df) / pf.stats()["Period"].days
