from dataclasses import dataclass

WEIGHTS = {"momentum": 0.30, "quality": 0.30, "catalysts": 0.25, "valuation": 0.15}

def clamp01(x: float | None) -> float:
    if x is None:
        return 0.0
    try:
        return max(0.0, min(1.0, float(x)))
    except Exception:
        return 0.0

@dataclass
class ScoreResult:
    score: int
    factors: dict
    why_summary: str

def compute_ai_score(momentum=None, quality=None, catalysts=None, valuation=None) -> ScoreResult:
    m = clamp01(momentum)
    q = clamp01(quality)
    c = clamp01(catalysts)
    v = clamp01(valuation)

    score01 = (
        WEIGHTS["momentum"] * m +
        WEIGHTS["quality"] * q +
        WEIGHTS["catalysts"] * c +
        WEIGHTS["valuation"] * v
    )
    score = round(score01 * 100)

    parts = []
    parts.append("momentum hot" if m > 0.7 else "momentum building" if m > 0.5 else "")
    parts.append("solid quality" if q > 0.7 else "improving quality" if q > 0.5 else "")
    if c > 0.6:
        parts.append("fresh catalysts")
    if v > 0.7:
        parts.append("undervalued")
    why = " · ".join([p for p in parts if p]) or "balanced setup"

    return ScoreResult(score=score, factors={"mom": m, "qual": q, "cat": c, "val": v}, why_summary=why[:140])
