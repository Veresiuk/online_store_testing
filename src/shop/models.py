from dataclasses import dataclass, field
from shop.exceptions import ValidationError
from shop.value_objects import Money


@dataclass(frozen=True, slots=True)
class Product:
    product_id: int
    name: str
    category: str
    price: float
    quantity: int

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValidationError(f"Ціна не може бути від'ємною: {self.price}")
        if self.quantity < 0:
            raise ValidationError(f"Кількість не може бути від'ємною: {self.quantity}")
        if not self.name.strip():
            raise ValidationError("Назва товару не може бути порожньою")

    @property
    def total_cost(self) -> float:
        """Вартість залишків конкретного товару на складі."""
        return self.price * self.quantity


@dataclass
class CartItem:
    product: Product
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")

    @property
    def total(self) -> float:
        return self.product.price * self.quantity


@dataclass
class Cart:
    items: list[CartItem] = field(default_factory=list)

    def add(self, product: Product, quantity: int = 1) -> None:
        self.items.append(CartItem(product, quantity))

    def __len__(self) -> int:
        return len(self.items)

    def __contains__(self, product_id: int) -> bool:
        return any(item.product.product_id == product_id for item in self.items)

    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)