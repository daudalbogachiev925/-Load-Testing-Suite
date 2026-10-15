from src.metrics import compute_metrics, percentile

def test_percentile_basic():
    values = list(range(1, 101))
    assert percentile(values, 50) == 50
    assert percentile(values, 95) == 95
    assert percentile(values, 99) == 99

def test_compute_metrics_empty():
    assert compute_metrics([]) == {}

def test_compute_metrics():
    results = [
        {"duration_ms": 100, "error": False, "step": "a", "elapsed_sec": 1, "user": 1},
        {"duration_ms": 200, "error": False, "step": "a", "elapsed_sec": 1, "user": 2},
        {"duration_ms": 300, "error": True, "step": "b", "elapsed_sec": 2, "user": 1},
    ]
    m = compute_metrics(results)
    assert m["requests"] == 3
    assert m["errors"] == 1
    assert abs(m["error_rate_pct"] - 33.33) < 1
    assert m["min_ms"] == 100
    assert m["max_ms"] == 300
