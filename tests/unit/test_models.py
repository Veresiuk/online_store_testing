import pytest
from shop.exceptions import ValidationError
from shop.models import Product


def test_product_creation_valid():
    p = Product(1, "Стіл", "Меблі", 1500.0, 4)
    assert p.product_id == 1
    assert p.name == "Стіл"
    assert p.category == "Меблі"
    assert p.total_cost == pytest.approx(6000.0)


@pytest.mark.parametrize(
    "price, quantity",
    [
        (0.0, 0),
        (0.01, 1),
        (100.0, 9999),
    ],
    ids=["zero_boundary", "min_positive_boundary", "standard_values"],
)
def test_product_boundary_values(price, quantity):
    p = Product(1, "Товар", "Категорія", price, quantity)
    assert p.price == pytest.approx(price)
    assert p.quantity == quantity


@pytest.mark.parametrize(
    "price, quantity, name, error_match",
    [
        (-0.01, 5, "Товар", "Ціна не може бути від'ємною"),
        (-100.0, 5, "Товар", "Ціна не може бути від'ємною"),
        (100.0, -1, "Товар", "Кількість не може бути від'ємною"),
        (100.0, 5, "   ", "Назва товару не може бути порожньою"),
    ],
    ids=["negative_boundary_price", "negative_price", "negative_quantity", "blank_name"],
)
def test_product_validation_errors(price, quantity, name, error_match):
    with pytest.raises(ValidationError, match=error_match):
        Product(1, name, "Категорія", price, quantity)