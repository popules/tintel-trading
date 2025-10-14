from collections import deque

def rsi14(prices: list[float], period: int = 14) -> float | None:
    if len(prices) < period + 1:
        return None
    gains, losses = 0.0, 0.0
    for i in range(1, period + 1):
        delta = prices[i] - prices[i-1]
        gains += max(delta, 0)
        losses += max(-delta, 0)
    if losses == 0:
        return 100.0
    avg_gain, avg_loss = gains / period, losses / period
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    for i in range(period + 1, len(prices)):
        delta = prices[i] - prices[i-1]
        gain = max(delta, 0)
        loss = max(-delta, 0)
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        rs = avg_gain / avg_loss if avg_loss != 0 else 0
        rsi = 100 - (100 / (1 + rs))
    return rsi
