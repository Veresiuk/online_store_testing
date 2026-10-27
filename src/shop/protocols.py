from typing import Protocol
from shop.models import Product


class ProductRepository(Protocol):
    """Інтерфейс для сховища товарів."""
    def get_by_id(self, product_id: int) -> Product | None:
        ...

    def get_all(self) -> list[Product]:
        ...

    def add(self, product: Product) -> None:
        ...


class DiscountPolicy(Protocol):
    """Інтерфейс для розрахунку знижок."""
    def apply_discount(self, total: float) -> float:
        ...


class ExternalInventoryProvider(Protocol):
    """Асинхронний інтерфейс зовнішнього постачальника."""
    async def fetch_stock_update(self, product_id: int) -> int:
        ...
        
class PaymentGateway(Protocol):
    def pay(self, amount: float) -> str:
        ...


class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> None:
        ...