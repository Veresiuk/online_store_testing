import os


def get_min_stock_threshold() -> int:
    """Повертає мінімальний поріг залишків на складі із середовища (env var)."""
    val = os.getenv("MIN_STOCK_THRESHOLD", "5")
    try:
        threshold = int(val)
        if threshold < 0:
            return 5
        return threshold
    except ValueError:
        return 5

def get_payment_mode() -> str:
    """Повертає поточний платіжний режим із середовища."""
    return os.getenv("PAYMENT_MODE", "sandbox")