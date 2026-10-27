import pytest
from shop.models import Cart, Product
from shop.services import (
    AsyncPaymentStatus,
    CheckoutService,
    PaymentError,
    PercentageDiscount,
)
from shop.protocols import Notifier, PaymentGateway
from unittest.mock import AsyncMock, Mock


def test_cart_operations():
    cart = Cart()
    p1 = Product(1, "Товар 1", "Кат", 100.0, 5)
    p2 = Product(2, "Товар 2", "Кат", 200.0, 5)

    cart.add(p1, 2)
    cart.add(p2, 1)

    assert len(cart) == 2
    assert 1 in cart
    assert 99 not in cart
    assert cart.total == pytest.approx(400.0)


def test_cart_item_invalid_quantity():
    p = Product(1, "Товар", "Кат", 100.0, 5)
    cart = Cart()
    with pytest.raises(ValueError, match="positive"):
        cart.add(p, 0)


def test_percentage_discount():
    discount = PercentageDiscount(10.0)
    assert discount.apply(200.0) == pytest.approx(180.0)
    assert discount.apply_discount(100.0) == pytest.approx(90.0)

    with pytest.raises(ValueError, match="Invalid discount"):
        PercentageDiscount(-5.0)


def test_checkout_service_success():
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.pay.return_value = "PAY-123"
    mock_notifier = Mock(spec=Notifier)

    cart = Cart()
    cart.add(Product(1, "Товар", "Кат", 100.0, 5), 1)

    service = CheckoutService(mock_gateway, mock_notifier)
    payment_id = service.checkout("test@example.com", cart)

    assert payment_id == "PAY-123"
    mock_gateway.pay.assert_called_once_with(100.0)
    mock_notifier.send.assert_called_once()


def test_checkout_service_empty_cart_raises():
    service = CheckoutService(Mock(spec=PaymentGateway), Mock(spec=Notifier))
    with pytest.raises(ValueError, match="Cart is empty"):
        service.checkout("test@example.com", Cart())


@pytest.mark.asyncio
async def test_async_payment_status():
    mock_client = AsyncMock()
    mock_client.fetch_status.return_value = {"status": "completed"}

    status_service = AsyncPaymentStatus(mock_client)
    res = await status_service.get_status("PAY-1")

    assert res == "completed"
    mock_client.fetch_status.assert_awaited_once_with("PAY-1")