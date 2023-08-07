import numpy as np
from numba import njit


# @njit(cache=True, parallel=True)
def cross_below_nb(arr1, arr2):
    cross_below_mask = np.logical_and(arr1[:-1] > arr2[:-1], arr1[1:] < arr2[1:])

    cross_below_mask = np.insert(cross_below_mask, 0, False)
    return cross_below_mask


def cross_below(arr1, arr2):
    return cross_below_nb(arr1.values, arr2.values)
