import numpy as np


def get_realized_pf_value(pf):
    original_equity = pf.get_value()
    equity = np.full_like(pf.orders.mask, original_equity[0], dtype=int)

    short_orders = np.full_like(pf.orders.mask, 0, dtype=int)
    long_orders = np.full_like(pf.orders.mask, 0, dtype=int)

    for order in pf.orders.records_arr:
        row = order[3]
        if order[8] == 1:
            short_orders[row] = order[6]
        else:
            long_orders[row] = order[6]

    for i, row in enumerate(short_orders):
        if row != 0 or long_orders[i] != 0:
            equity[i] = original_equity[i]
        else:
            equity[i] = equity[i - 1]
    return equity
