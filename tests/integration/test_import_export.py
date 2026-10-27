import json
import pytest
from shop.exceptions import MalformedRecordError
from shop.exporters import export_products_to_json, import_products_from_csv
from shop.models import Product


@pytest.mark.integration
def test_csv_import_success(tmp_path):
    csv_file = tmp_path / "products.csv"
    csv_file.write_text(
        "id,name,category,price,quantity\n"
        "1,Чайник,Побутова техніка,1200.5,5\n"
        "2,Праска,Побутова техніка,2500.0,2\n",
        encoding="utf-8",
    )

    items = import_products_from_csv(csv_file)

    assert len(items) == 2
    assert items[0].name == "Чайник"
    assert items[0].price == pytest.approx(1200.5)


@pytest.mark.integration
def test_csv_import_malformed_record_raises(tmp_path):
    csv_file = tmp_path / "malformed.csv"
    csv_file.write_text(
        "id,name,category,price,quantity\n"
        "1,Чайник,Побутова техніка,bad_price,5\n",
        encoding="utf-8",
    )

    with pytest.raises(MalformedRecordError, match="Помилка у рядку 2"):
        import_products_from_csv(csv_file)


@pytest.mark.integration
def test_csv_import_missing_file_raises(tmp_path):
    missing_file = tmp_path / "non_existing.csv"
    with pytest.raises(FileNotFoundError):
        import_products_from_csv(missing_file)


@pytest.mark.integration
def test_export_and_read_json(tmp_path):
    json_file = tmp_path / "export.json"
    products = [
        Product(10, "Навушники", "Аудіо", 1500.0, 2),
    ]

    export_products_to_json(products, json_file)

    assert json_file.exists()
    data = json.loads(json_file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["name"] == "Навушники"
    assert data[0]["total_cost"] == pytest.approx(3000.0)