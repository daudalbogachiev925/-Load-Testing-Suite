def percentile(values, p):
    if not values:
        return 0
    s = sorted(values)
    k = int(len(s) * p / 100)
    return round(s[min(k, len(s) - 1)], 2)

def compute_metrics(results):
    if not results:
        return {}
    durations = [r["duration_ms"] for r in results]
    errors = [r for r in results if r["error"]]
    return {
        "requests": len(results),
        "errors": len(errors),
        "error_rate_pct": round(len(errors) / len(results) * 100, 2),
        "p50_ms": percentile(durations, 50),
        "p75_ms": percentile(durations, 75),
        "p90_ms": percentile(durations, 90),
        "p95_ms": percentile(durations, 95),
        "p99_ms": percentile(durations, 99),
        "avg_ms": round(sum(durations) / len(durations), 2),
        "min_ms": min(durations),
        "max_ms": max(durations),
    }

def throughput_by_second(results):
    by_second = {}
    for r in results:
        s = int(r.get("elapsed_sec", 0))
        by_second[s] = by_second.get(s, 0) + 1
    return by_second

def metrics_by_step(results):
    by_step = {}
    for r in results:
        step = r["step"]
        by_step.setdefault(step, []).append(r)
    return {step: compute_metrics(rs) for step, rs in by_step.items()}

def concurrent_users(results):
    by_second = {}
    for r in results:
        s = int(r.get("elapsed_sec", 0))
        by_second.setdefault(s, set()).add(r["user"])
    return {s: len(u) for s, u in by_second.items()}
