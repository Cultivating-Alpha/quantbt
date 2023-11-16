def resample(df, tf="1H"):
    return (
        df.resample(tf)
        .agg(
            {
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                # "volume": "sum",
            }
        )
        .dropna(how="all")
        .fillna(method="ffill")
    )
