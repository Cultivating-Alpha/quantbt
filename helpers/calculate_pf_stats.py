from helpers.analyze_trade_duration import analyze_trade_duration


def calculate_pf_stats(pf, size, multiplier):
    number_of_months = pf.stats()["Period"].days / 30
    stats = pf.stats()

    end = stats["End Value"]
    trades = stats["Total Trades"]
    init_cash = stats["Start Value"]

    monthly = (end - init_cash) / number_of_months
    avg = monthly / init_cash * 100
    trades = stats["Total Trades"]
    lots_per_month = trades / number_of_months * size
    short_trades_per_day = analyze_trade_duration(pf)
    tnx_cost = trades * 2 * 0.25 * size * multiplier

    # Get quarterly
    # quarterly = df.resample("Q").agg(["last", "first"])
    # quarterly["diff"] = quarterly["last"] - quarterly["first"]
    # quarterly["diff"].sum()
    # quarterly["diff"].mean()
    #
    return [
        init_cash,
        monthly,
        avg,
        lots_per_month,
        short_trades_per_day,
        stats["Total Trades"] / number_of_months,
        tnx_cost / number_of_months,
        stats["Min Value"],
        end,
    ]
