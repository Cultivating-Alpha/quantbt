from quantnb.core.enums import CommissionType
from numba import njit


@njit(cache=True)
def calculate_commission(commission_type, commission, price, volume) -> float:
    if commission_type == CommissionType.FIXED.value:
        return commission
    elif commission_type == CommissionType.PERCENTAGE.value:
        return price * volume * commission / 100
    else:
        return commission
