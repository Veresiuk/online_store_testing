from shop.exceptions import EmptyCatalogError, ProductNotFoundError, ValidationError
from shop.models import Product
from shop.protocols import DiscountPolicy, ExternalInventoryProvider, ProductRepository


class CatalogService:
    def __init__(self, repository: ProductRepository) -> None:
        self._repo = repository

    def add_product(self, product: Product) -> None:
        self._repo.add(product)

    def find_product(self, product_id: int) -> Product:
        item = self._repo.get_by_id(product_id)
        if item is None:
            raise ProductNotFoundError(f"Товар з ID {product_id} не знайдено.")
        return item

    def filter_by_category(self, category: str) -> list[Product]:
        return [p for p in self._repo.get_all() if p.category.lower() == category.lower()]

    def calculate_total_inventory_value(self, discount_policy: DiscountPolicy | None = None) -> float:
        items = self._repo.get_all()
        total = sum(p.total_cost for p in items)
        if discount_policy is not None:
            return discount_policy.apply_discount(total)
        return total

    def get_most_expensive_product(self) -> Product:
        items = self._repo.get_all()
        if not items:
            raise EmptyCatalogError("Каталог порожній")
        return max(items, key=lambda p: p.price)

    async def sync_stock_with_provider(
        self, product_id: int, provider: ExternalInventoryProvider
    ) -> Product:
        current_product = self.find_product(product_id)
        new_quantity = await provider.fetch_stock_update(product_id)
        if new_quantity < 0:
            raise ValidationError("Провайдер повернув некоректну кількість")

        updated = Product(
            product_id=current_product.product_id,
            name=current_product.name,
            category=current_product.category,
            price=current_product.price,
            quantity=new_quantity,
        )
        self._repo.add(updated)
        return updated