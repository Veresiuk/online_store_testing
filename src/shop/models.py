from dataclasses import dataclass
from shop.exceptions import ValidationError


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