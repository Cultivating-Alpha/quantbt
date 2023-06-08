import pandas as pd


def print_orders(orders_arr):
    # Convert the numpy arrays to dataframes
    orders_df = pd.DataFrame(
        orders_arr, columns=["timestamp", "action", "price", "size", "cash"]
    )
    orders_df["action"] = orders_df["action"].apply(
        lambda x: "buy" if x == 1 else "sell"
    )
    print(orders_df)
    return orders_df
