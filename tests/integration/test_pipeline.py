import json
from unittest.mock import AsyncMock
import pytest
from shop.exporters import export_products_to_json, import_products_from_csv
from shop.protocols import ExternalInventoryProvider
from shop.services import CatalogService


@pytest.mark.integration
@pytest.mark.asyncio
async def test_full_shop_lifecycle_pipeline(tmp_path, empty_repo):
    # 1. Створення тимчасового CSV із тестовими даними
    input_csv = tmp_path / "catalog_in.csv"
    output_json = tmp_path / "catalog_out.json"
    input_csv.write_text(
        "id,name,category,price,quantity\n"
        "1,Планшет,Гаджети,12000.0,2\n"
        "2,Чохол,Аксесуари,500.0,10\n",
        encoding="utf-8",
    )

    # 2. Імпорт товарів і збереження у сховищі (використовуємо empty_repo як InMemoryProductRepository)
    items = import_products_from_csv(input_csv)
    service = CatalogService(empty_repo)
    for product in items:
        service.add_product(product)

    # 3. Асинхронна синхронізація залишків через Mock
    mock_provider = AsyncMock(spec=ExternalInventoryProvider)
    mock_provider.fetch_stock_update.return_value = 5  # оновлено залишок для ID 1
    await service.sync_stock_with_provider(1, mock_provider)

    # 4. Експорт оновленого каталогу в JSON
    all_items = empty_repo.get_all()
    export_products_to_json(all_items, output_json)

    # 5. Верифікація результатів згенерованого файлу
    exported_data = json.loads(output_json.read_text(encoding="utf-8"))
    tablet_item = next(p for p in exported_data if p["id"] == 1)

    assert tablet_item["quantity"] == 5
    assert tablet_item["total_cost"] == pytest.approx(60000.0)
    assert service.get_most_expensive_product().name == "Планшет"