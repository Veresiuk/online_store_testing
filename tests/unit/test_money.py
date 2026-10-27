import pytest
from shop.value_objects import Money


def test_money_creation():
    m = Money(100.0, "UAH")
    assert m.amount == pytest.approx(100.0)
    assert m.currency == "UAH"


def test_money_negative_amount_raises():
    with pytest.raises(ValueError, match="negative"):
        Money(-10.0)


def test_money_addition():
    m1 = Money(150.0)
    m2 = Money(50.0)
    total = m1 + m2
    assert total.amount == pytest.approx(200.0)


def test_money_currency_mismatch():
    with pytest.raises(ValueError, match="Currency mismatch"):
        _ = Money(100.0, "UAH") + Money(100.0, "USD")