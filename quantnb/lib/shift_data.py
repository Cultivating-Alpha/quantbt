from numba import njit
import numpy as np


@njit(parallel=True, cache=True)
def shift_data(arr, shift):
    new_arr = np.empty_like(arr)

    for i in range(len(arr)):
        new_arr[i] = arr[i + shift]
    return new_arr
