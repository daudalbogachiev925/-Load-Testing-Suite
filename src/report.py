import json
from datetime import datetime

def to_json(results, path="load_report.json"):
    from src.metrics import compute_metrics, metrics_by_step
    report = {
        "generated_at": datetime.utcnow().isoformat(),
        "summary": compute_metrics(results),
        "by_step": metrics_by_step(results),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return report

def to_markdown(results):
    from src.metrics import compute_metrics
    m = compute_metrics(results)
    lines = ["# Load Test Report", ""]
    lines.append(f"**Generated:** {datetime.utcnow().isoformat()}")
    lines.append("")
    lines.append("## Summary")
    for k, v in m.items():
        lines.append(f"- **{k}**: {v}")
    return "\n".join(lines)
