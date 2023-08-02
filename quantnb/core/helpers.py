import numpy as np
from numba import njit


@njit
def print_bar(length, fill, iteration, total, prev_percentage):
    percentage = iteration * 100 / total
    print("AS")
    if percentage - prev_percentage > 10:
        progress = iteration / float(total)
        filled_length = int(length * progress)
        bar = fill * filled_length + "-" * (length - filled_length)
        print(np.round(percentage), f"% | {bar} |")
        return percentage
