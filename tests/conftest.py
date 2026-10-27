import pytest
from shop.models import Product
from shop.protocols import ProductRepository


class InMemoryProductRepository(ProductRepository):
    """Fake-репозиторій для ізольованого тестування логіки без зовнішніх БД."""
    def __init__(self) -> None:
        self._storage: dict[int, Product] = {}

    def get_by_id(self, product_id: int) -> Product | None:
        return self._storage.get(product_id)

    def get_all(self) -> list[Product]:
        return list(self._storage.values())

    def add(self, product: Product) -> None:
        self._storage[product.product_id] = product


@pytest.fixture
def empty_repo() -> InMemoryProductRepository:
    return InMemoryProductRepository()


@pytest.fixture
def sample_products() -> list[Product]:
    return [
        Product(1, "Ноутбук", "Електроніка", 25000.0, 3),
        Product(2, "Мишка", "Електроніка", 500.0, 10),
        Product(3, "Кава", "Продукти", 250.0, 20),
    ]


@pytest.fixture
def populated_repo(
    empty_repo: InMemoryProductRepository, sample_products: list[Product]
) -> InMemoryProductRepository:
    for item in sample_products:
        empty_repo.add(item)
    return empty_repo