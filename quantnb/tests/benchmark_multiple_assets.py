def benchmark_multiple_assets(assets):
    values = []
    for asset in assets:
        values.append(
            [
                asset.split("data/")[1].split(".parquet")[0],
                bt.data.index[0],
                len(bt.data),
                bt.stats["total_return"][0],
                bt.stats["buy_and_hold"][0],
            ]
        )

    df = pd.DataFrame(
        values,
        columns=[
            "symbol",
            "Start Date",
            "Candles",
            "Strategy Return [%]",
            "Buy and Hold [%]",
        ],
    )

    df = df.sort_values(by=["Start Date"], ascending=True)
    df.set_index("symbol", inplace=True)
    df
