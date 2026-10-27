from shop.config import get_min_stock_threshold
from shop.config import get_payment_mode

def test_min_stock_threshold_custom_env(monkeypatch):
    monkeypatch.setenv("MIN_STOCK_THRESHOLD", "12")
    assert get_min_stock_threshold() == 12


def test_min_stock_threshold_default(monkeypatch):
    monkeypatch.delenv("MIN_STOCK_THRESHOLD", raising=False)
    assert get_min_stock_threshold() == 5


def test_min_stock_threshold_invalid_string(monkeypatch):
    monkeypatch.setenv("MIN_STOCK_THRESHOLD", "not_a_number")
    assert get_min_stock_threshold() == 5


def test_min_stock_threshold_negative_env(monkeypatch):
    monkeypatch.setenv("MIN_STOCK_THRESHOLD", "-7")
    assert get_min_stock_threshold() == 5
    

def test_payment_mode(monkeypatch):
    assert get_payment_mode() == "sandbox"
    monkeypatch.setenv("PAYMENT_MODE", "production")
    assert get_payment_mode() == "production"