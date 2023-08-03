from quantnb.core.enums import CommissionType
from numba import njit


@njit(cache=True)
def calculate_commission(commission_type, commission, price):
    if commission_type == CommissionType.FIXED:
        return commission
    elif commission_type == CommissionType.PERCENTAGE:
        print("here")
        return price * commission / 100
