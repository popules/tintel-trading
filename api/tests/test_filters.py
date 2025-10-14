from app.utils.filters import quality_gates

def test_quality_gates():
    ok = {
        "price": 4.9, "market_cap": 120_000_000, "float": 25_000_000,
        "adv20": 2_500_000, "revenue_ttm": 30_000_000, "exchange": "NASDAQ"
    }
    bad = {**ok, "price": 6}
    assert quality_gates(ok) is True
    assert quality_gates(bad) is False
