from src.metrics import compute_metrics, metrics_by_step

def find_bottlenecks(results, threshold_p95=500):
    by_step = metrics_by_step(results)
    bottlenecks = []
    for step, m in by_step.items():
        if m["p95_ms"] > threshold_p95 or m["error_rate_pct"] > 5:
            bottlenecks.append({
                "step": step,
                "p95_ms": m["p95_ms"],
                "error_rate_pct": m["error_rate_pct"],
                "reason": "high latency" if m["p95_ms"] > threshold_p95
                          else "high error rate",
            })
    return sorted(bottlenecks, key=lambda x: -x["p95_ms"])

def sla_check(results, sla_p95=1000, sla_error_rate=1.0):
    m = compute_metrics(results)
    return {
        "p95_ok": m["p95_ms"] <= sla_p95,
        "error_rate_ok": m["error_rate_pct"] <= sla_error_rate,
        "p95_ms": m["p95_ms"],
        "error_rate_pct": m["error_rate_pct"],
        "sla_p95": sla_p95,
        "sla_error_rate": sla_error_rate,
        "passed": m["p95_ms"] <= sla_p95 and m["error_rate_pct"] <= sla_error_rate,
    }

def recommend_scaling(results):
    m = compute_metrics(results)
    if m.get("p95_ms", 0) > 2000:
        return "Добавить серверов приложения (RAS) — p95 критический"
    if m.get("p95_ms", 0) > 1000:
        return "Оптимизировать запросы или добавить рабочие процессы"
    if m.get("error_rate_pct", 0) > 5:
        return "Проверить блокировки и ошибки подключения"
    return "Производительность в норме"
