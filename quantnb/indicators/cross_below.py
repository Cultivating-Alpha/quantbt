import numpy as np


def cross_below(arr1, arr2):
    cross_below_mask = np.logical_and(arr1[:-1] > arr2[:-1], arr1[1:] < arr2[1:])

    cross_below_mask = np.insert(cross_below_mask, 0, False)
    return cross_below_mask
