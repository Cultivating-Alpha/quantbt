def resample(df, tf="1H"):
    df.resample(tf).agg(
        {
            "Open": "first",
            "High": "max",
            "Low": "min",
            "Close": "last",
            "volume": "sum",
        }
    ).fillna(method="ffill")
