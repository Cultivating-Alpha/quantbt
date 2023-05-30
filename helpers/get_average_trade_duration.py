def get_average_trade_duration(pf):
    df = pf.trades.records_readable
    entries = df["Entry Index"]
    exists = df["Exit Index"]
    diff = exists - entries
    df["diff"] = diff
    return df["diff"].mean()
