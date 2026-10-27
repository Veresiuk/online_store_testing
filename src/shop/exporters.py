import csv
import json
from pathlib import Path
from shop.exceptions import MalformedRecordError
from shop.models import Product


def import_products_from_csv(file_path: Path) -> list[Product]:
    products: list[Product] = []
    if not file_path.exists():
        raise FileNotFoundError(f"Файл не знайдено: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_idx, row in enumerate(reader, start=2):
            try:
                products.append(
                    Product(
                        product_id=int(row["id"]),
                        name=row["name"],
                        category=row["category"],
                        price=float(row["price"]),
                        quantity=int(row["quantity"]),
                    )
                )
            except (KeyError, ValueError, TypeError) as err:
                raise MalformedRecordError(
                    f"Помилка у рядку {row_idx}: некоректні дані"
                ) from err
    return products


def export_products_to_json(products: list[Product], output_path: Path) -> None:
    data = [
        {
            "id": p.product_id,
            "name": p.name,
            "category": p.category,
            "price": p.price,
            "quantity": p.quantity,
            "total_cost": p.total_cost,
        }
        for p in products
    ]
    output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")