import numpy as np
from numba import njit, prange


@njit(cache=True, nogil=True)
def Donchian(high, low, donchian_len, offset=0):
    donchian = np.full_like(high, np.nan, dtype=np.float_)
    indicator = np.full_like(high, np.nan, dtype=np.float_)
    for i in range(donchian_len, high.shape[0]):
        # Calculate the middle of highest and lowest in window
        highest = np.max(high[i - donchian_len : i])
        lowest = np.min(low[i - donchian_len : i])
        donchian[i] = (highest + lowest) / 2

    for i in range(donchian_len + offset + 1, high.shape[0]):
        indicator[i] = donchian[i - offset]

    return indicator


@njit(cache=True, nogil=True)
def p_Donchian(high, low, donchian_len, offset=0):
    donchian = np.full_like(high, np.nan, dtype=np.float_)
    indicator = np.full_like(high, np.nan, dtype=np.float_)
    for i in prange(donchian_len, high.shape[0]):
        # Calculate the middle of highest and lowest in window
        highest = np.max(high[i - donchian_len : i])
        lowest = np.min(low[i - donchian_len : i])
        donchian[i] = (highest + lowest) / 2

    for i in range(donchian_len + offset + 1, high.shape[0]):
        indicator[i] = donchian[i - offset]

    return indicator
