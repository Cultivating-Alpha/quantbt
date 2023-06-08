import pandas as pd


def combine_files(asset):
    import os

    # Specify the directory path
    directory = "./optimisation"

    # Get all files under the directory
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)

    files = [item for item in file_list if asset in item]
    df = pd.DataFrame()
    for file in files:
        df = pd.concat([df, pd.read_parquet(file)])
    df.sort_values("long", inplace=True)

    df.to_parquet(f"./optimisation/{asset}.full.parquet")
    return df


# df = combine_files("WETH-USDC")
# df = combine_files("WMATIC-USDC")
