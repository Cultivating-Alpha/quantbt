from numba import float32, int32, int64, float64

data_specs = [
    ("close", float32[:]),
    ("date", int64[:]),
    ("data_type", int32),
    ("open", float32[:]),
    ("high", float32[:]),
    ("low", float32[:]),
    ("volume", float32[:]),
    ("bid", float32[:]),
    ("ask", float32[:]),
    ("initial_capital", float32),
    ("final_value", float32),
    ("total_pnl", float32),
    ("equity", float32[:]),
]

trade_specs = [
    ("data_type", int32),
    ("active_trades", float64[:, :]),
    ("last_active_trade_index", int32),
    ("closed_trades", float64[:, :]),
    ("last_closed_trade_index", int32),
    ("multiplier", float32),
]

backtester_specs = [
    ("prev_percentage", float32),
    ("commission", float32),
    ("commission_type", int32),
    ("slippage", float32),
    ("slippage_type", int32),
]
