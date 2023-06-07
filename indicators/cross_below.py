import numpy as np


def cross_below(arr1, arr2):
    cross_below_mask = np.logical_and(arr1[:-1] > arr2[:-1], arr1[1:] < arr2[1:])
    return cross_below_mask
