class ShopException(Exception):
    """Базовий виняток інтернет-магазину."""


class ValidationError(ShopException):
    """Помилка валідації вхідних даних чи стану об'єкта."""


class MalformedRecordError(ShopException):
    """Помилка некоректного формату запису при завантаженні/імпорті."""


class ProductNotFoundError(ShopException):
    """Виняток, коли запитуваний товар відсутній у каталозі."""


class EmptyCatalogError(ShopException):
    """Виняток при спробі виконання операцій над порожнім каталогом."""


class ExternalProviderError(ShopException):
    """Помилка взаємодії із зовнішнім провайдером залишків."""