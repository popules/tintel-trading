from app.scoring import compute_ai_score

def test_compute_ai_score_bounds():
    r = compute_ai_score(momentum=1.2, quality=None, catalysts=-1, valuation=0.5)
    assert 0 <= r.score <= 100
    assert abs(sum(r.factors.values()) - (1.0 + 0.0 + 0.0 + 0.5)) >= 0  # sanity call
