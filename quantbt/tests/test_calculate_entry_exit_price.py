from quantnb.core import calculate_entry_price, calculate_exit_price
from quantnb.core.enums import OrderDirection
import timeit


class Timing:
    def timeit(self, _lambda, number=10000):
        duration = timeit.timeit(lambda: _lambda, number=10000)
        value = _lambda
        return value, duration


class TestCalculatePrice:
    slippage = 0.1
    direction_long = OrderDirection.LONG.value
    direction_short = OrderDirection.SHORT.value
    price = 100.0
    bid = 99.8
    ask = 100.2

    def test_long(self):
        value = calculate_entry_price(
            self.slippage, self.direction_long, price_value=self.price
        )
        assert value == self.price + self.slippage

    def test_short(self):
        value = calculate_entry_price(
            self.slippage, self.direction_short, price_value=self.price
        )
        assert value == self.price - self.slippage

    def test_no_slippage(self):
        value = calculate_entry_price(0, self.direction_short, price_value=self.price)
        assert value == self.price

    def test_long_bidask(self):
        value = calculate_entry_price(
            self.slippage, self.direction_long, bid=self.bid, ask=self.ask
        )
        assert value == self.ask + self.slippage

    def test_short_bidask(self):
        value = calculate_entry_price(
            self.slippage, self.direction_short, bid=self.bid, ask=self.ask
        )
        assert value == self.bid - self.slippage

    def test_no_slippage_bidask(self):
        value = calculate_entry_price(
            0, self.direction_short, bid=self.bid, ask=self.ask
        )
        assert value == self.bid


class TestCalculateExitPrice:
    slippage = 0.1
    direction_long = OrderDirection.LONG.value
    direction_short = OrderDirection.SHORT.value
    price = 100.0
    bid = 99.8
    ask = 100.2

    def test_long(self):
        value = calculate_exit_price(
            self.slippage, self.direction_long, price_value=self.price
        )
        assert value == self.price - self.slippage

    def test_short(self):
        value = calculate_exit_price(
            self.slippage, self.direction_short, price_value=self.price
        )
        assert value == self.price + self.slippage

    def test_no_slippage(self):
        value = calculate_exit_price(0, self.direction_short, price_value=self.price)
        assert value == self.price

    def test_long_bidask(self):
        value = calculate_exit_price(
            self.slippage, self.direction_long, bid=self.bid, ask=self.ask
        )
        assert value == self.bid - self.slippage

    def test_short_bidask(self):
        value = calculate_exit_price(
            self.slippage, self.direction_short, bid=self.bid, ask=self.ask
        )
        assert value == self.ask + self.slippage

    def test_no_slippage_bidask(self):
        value = calculate_exit_price(
            0, self.direction_short, bid=self.bid, ask=self.ask
        )
        assert value == self.ask
