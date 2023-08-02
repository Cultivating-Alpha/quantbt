from numba import njit


@njit
def calculate_fees(price, size, commission, commission_type):
    if commission_type == "percentage":
        return price * size * commission
    else:
        return commission
