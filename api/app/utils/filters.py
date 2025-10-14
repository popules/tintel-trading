def quality_gates(item: dict) -> bool:
    # Default quality filters
    price = item.get("price") or 0
    mcap = item.get("market_cap") or 0
    flt = item.get("float") or 0
    adv20 = item.get("adv20") or 0
    rev = item.get("revenue_ttm") or 0
    exchange = item.get("exchange") or ""

    if price <= 0 or price > 5:
        return False
    if mcap < 100_000_000:
        return False
    if flt < 20_000_000:
        return False
    if adv20 < 2_000_000:
        return False
    if rev < 25_000_000:
        return False
    if exchange.upper() not in {"NASDAQ","NYSE","AMEX"}:
        return False
    return True
