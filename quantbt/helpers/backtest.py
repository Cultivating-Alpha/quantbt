def backtest(
    strategy_vars=None,
    strategy=None,
    data=None,
    signal_params=None,
    backtest_vars=None,
):
    if data is None:
        print("Please provide data data")
        return None

    if strategy is None:
        print("Please provide a valid strategy")
        return None

    st = strategy(data, strategy_vars)

    st.set_backtester_settings(**backtest_vars)
    st.from_signals(signal_params)
    return st
