import matplotlib.pyplot as plt


def plot_lines(index, lines):
    for i, line in enumerate(lines):
        plt.plot(index, line, label=f"y{i}")
        # plt.plot(range(len(line)), line, label=f"y{i}")
    plt.xlabel("x-axis")
    plt.ylabel("y-axis")
    plt.title("Two lines on one plot")
    plt.legend()
    plt.show()
