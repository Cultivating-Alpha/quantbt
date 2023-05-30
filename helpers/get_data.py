import vectorbtpro as vbt


def get_data(steps):
    datas = {}
    for step in steps:
        df = vbt.HDFData.fetch(f"./data/@ENQ/{step}.h5")
        datas[step] = df
        # df = vbt.CSVData.fetch("tv.csv")
        # datas[step] = df[0:515]
        # datas[step] = df[50000:70000]
        # datas[step] = df[288107:288400]

    return datas
