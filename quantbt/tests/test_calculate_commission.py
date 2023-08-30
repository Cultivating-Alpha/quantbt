from quantnb.core import calculate_commission
from quantnb.core.enums import CommissionType


class TestCalculatePrice:
    price = 523
    commission_fixed = 7
    commission_percentage = 0.02

    def test_commission_fixed(self):
        volume = 0.4
        value = calculate_commission(
            CommissionType.FIXED, self.commission_fixed, self.price, volume
        )

        assert value == self.commission_fixed

    def test_commission_percentage(self):
        volume = 0.4
        value = calculate_commission(
            CommissionType.PERCENTAGE, self.commission_percentage, self.price, volume
        )

        assert value == self.price * self.commission_percentage * 0.4
