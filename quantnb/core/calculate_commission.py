from quantnb.core.enums import CommissionType
from numba import njit


@njit
def calculate_commission(commission_type, commission, price):
    if commission_type == CommissionType.FIXED:
        return commission
    elif commission_type == CommissionType.PERCENTAGE:
        return price * commission / 100
