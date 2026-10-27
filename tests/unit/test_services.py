from unittest.mock import AsyncMock, Mock
import pytest
from shop.exceptions import (
    EmptyCatalogError,
    ExternalProviderError,
    ProductNotFoundError,
    ValidationError,
)
from shop.models import Product
from shop.protocols import DiscountPolicy, ExternalInventoryProvider, ProductRepository
from shop.services import CatalogService


def test_add_and_find_product(empty_repo):
    service = CatalogService(empty_repo)
    product = Product(10, "Клавіатура", "Електроніка", 1200.0, 5)
    service.add_product(product)

    found = service.find_product(10)
    assert found == product


def test_find_product_not_found_raises(empty_repo):
    service = CatalogService(empty_repo)
    with pytest.raises(ProductNotFoundError, match="не знайдено"):
        service.find_product(999)


def test_filter_by_category(populated_repo):
    service = CatalogService(populated_repo)
    electronics = service.filter_by_category("Електроніка")
    assert len(electronics) == 2
    assert all(p.category == "Електроніка" for p in electronics)


def test_filter_by_category_case_insensitive(populated_repo):
    service = CatalogService(populated_repo)
    food = service.filter_by_category("продукти")
    assert len(food) == 1
    assert food[0].name == "Кава"


def test_calculate_total_inventory_value_without_discount(populated_repo):
    service = CatalogService(populated_repo)
    # 25000*3 + 500*10 + 250*20 = 75000 + 5000 + 5000 = 85000
    assert service.calculate_total_inventory_value() == pytest.approx(85000.0)


def test_calculate_total_inventory_with_discount_mock(populated_repo):
    service = CatalogService(populated_repo)
    discount_mock = Mock(spec=DiscountPolicy)
    discount_mock.apply_discount.return_value = 76500.0

    result = service.calculate_total_inventory_value(discount_policy=discount_mock)

    assert result == pytest.approx(76500.0)
    discount_mock.apply_discount.assert_called_once_with(85000.0)


def test_most_expensive_product(populated_repo):
    service = CatalogService(populated_repo)
    expensive = service.get_most_expensive_product()
    assert expensive.name == "Ноутбук"
    assert expensive.price == pytest.approx(25000.0)


def test_most_expensive_product_empty_catalog_raises(empty_repo):
    service = CatalogService(empty_repo)
    with pytest.raises(EmptyCatalogError, match="Каталог порожній"):
        service.get_most_expensive_product()


def test_empty_catalog_total_value(empty_repo):
    service = CatalogService(empty_repo)
    assert service.calculate_total_inventory_value() == 0.0


def test_repository_mock_interaction():
    mock_repo = Mock(spec=ProductRepository)
    mock_repo.get_by_id.return_value = Product(1, "Тест", "Кат", 100.0, 1)

    service = CatalogService(mock_repo)
    p = service.find_product(1)

    assert p.name == "Тест"
    mock_repo.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_sync_stock_with_provider_success(empty_repo):
    product = Product(1, "Монітор", "Електроніка", 8000.0, 2)
    empty_repo.add(product)
    service = CatalogService(empty_repo)

    mock_provider = AsyncMock(spec=ExternalInventoryProvider)
    mock_provider.fetch_stock_update.return_value = 15

    updated = await service.sync_stock_with_provider(1, mock_provider)

    assert updated.quantity == 15
    mock_provider.fetch_stock_update.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_sync_stock_with_provider_side_effect_failure(empty_repo):
    product = Product(1, "Монітор", "Електроніка", 8000.0, 2)
    empty_repo.add(product)
    service = CatalogService(empty_repo)

    mock_provider = AsyncMock(spec=ExternalInventoryProvider)
    mock_provider.fetch_stock_update.side_effect = ExternalProviderError("Network Down")

    with pytest.raises(ExternalProviderError, match="Network Down"):
        await service.sync_stock_with_provider(1, mock_provider)


@pytest.mark.asyncio
async def test_sync_stock_with_invalid_provider_response(empty_repo):
    product = Product(1, "Монітор", "Електроніка", 8000.0, 2)
    empty_repo.add(product)
    service = CatalogService(empty_repo)

    mock_provider = AsyncMock(spec=ExternalInventoryProvider)
    mock_provider.fetch_stock_update.return_value = -3

    with pytest.raises(ValidationError, match="некоректну кількість"):
        await service.sync_stock_with_provider(1, mock_provider)