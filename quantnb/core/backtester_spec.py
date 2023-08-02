from numba import float32, int32, int64, boolean

data = [
    ("open", float32[:]),
    ("high", float32[:]),
    ("low", float32[:]),
    ("close", float32[:]),
    ("volume", float32[:]),
    ("date", int64[:]),
]
bid_ask_data = [
    ("bid", float32[:]),
    ("ask", float32[:]),
]
portfolio = [
    ("initial_capital", float32),
    ("final_value", float32),
    ("total_pnl", float32),
    ("multiplier", float32),
    ("equity", float32[:]),
    ("size", float32),
    ("size_type", int32),
]
trade_management = [
    ("current_trade_type", int32),
    ("commission", float32),
    ("commission_type", int32),
    ("slippage", float32),
    ("slippage_type", int32),
    ("active_trades", float32[:, :]),
    ("closed_trades", float32[:, :]),
    ("number_of_closed_trades", int32),
]
misc = [
    ("order_idx", int32),
    ("trade_idx", int32),
    ("orders", float32[:, :]),
    ("trades", float32[:, :]),
    ("final_trades", float32[:, :]),
]
position_management = [
    ("total_volume", float32),
    ("weighted_sum", float32),
    ("average_price", float32),
]
general = [
    ("prev_percentage", float32),
]


spec = (
    data
    + bid_ask_data
    + portfolio
    + trade_management
    + misc
    + position_management
    + general
)
spec

# spec = [
#     # DATA
#     ("high", float32[:]),
#     ("low", float32[:]),
#     ("close", float32[:]),
#     ("volume", float32[:]),
#     ("date", int64[:]),
#     # Bid Ask Data
#     ("bid", float32[:]),
#     ("ask", float32[:]),
#     # PORTFOLIO
#     ("initial_capital", float32),
#     ("cash", float32),
#     ("final_value", float32),
#     ("total_pnl", float32),
#     ("multiplier", float32),
#     ("equity", float32[:]),
#     ("default_size", float32),
#     # TRADE MANAGEMENT
#     ("in_position", boolean),
#     ("stop_loss", float32),
#     ("entry_time", int32),
#     ("entry_size", float32),
#     ("entry_price", float32),
#     ("current_trade_type", int32),
#     ("commission", float32),
#     ("commission_type", int32),
#     ("slippage", float32),
#     ("slippage_type", int32),
#     # MISC
#     ("order_idx", int32),
#     ("trade_idx", int32),
#     ("orders", float32[:, :]),
#     ("trades", float32[:, :]),
#     ("final_trades", float32[:, :]),
#     # TRADE MANAGEMENT
#     ("active_trades", float32[:, :]),
#     ("closed_trades", float32[:, :]),
#     ("number_of_closed_trades", int32),
#     # POSITION MANAGEMENT
#     ("total_volume", float32),
#     ("weighted_sum", float32),
#     ("average_price", float32),
#     # GENERAL
#     ("prev_percentage", float32),
# ]
