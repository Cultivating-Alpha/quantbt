from quantnb.core.enums import CommissionType
from numba import njit


@njit
def calculate_commission(commission_type, commission, current_price, entry_price, volume) -> float:
    if commission_type == CommissionType.FIXED.value:
        return commission
    elif commission_type == CommissionType.PERCENTAGE.value:
        entry_commission = entry_price * volume * commission
        current_commission = current_price * volume * commission
        return entry_commission + current_commission
    else:
        return commission
