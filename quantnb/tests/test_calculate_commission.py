from quantnb.core import calculate_commission
from quantnb.core.enums import CommissionType


class TestCalculatePrice:
    price = 523
    commission_fixed = 7
    commission_percentage = 0.02

    def test_commission_fixed(self):
        value = calculate_commission(
            CommissionType.FIXED, self.commission_fixed, self.price
        )

        assert value == self.commission_fixed

    def test_commission_percentage(self):
        value = calculate_commission(
            CommissionType.PERCENTAGE, self.commission_percentage, self.price
        )

        assert value == self.price * self.commission_percentage / 100
