import time
import random
from datetime import datetime
from src.scenarios import Scenario
from src.generator import generate_users

class LoadRunner:
    def __init__(self, scenario: Scenario):
        self.scenario = scenario
        self.results = []

    def run(self, max_iterations=None):
        users = generate_users(self.scenario)
        start = datetime.utcnow()
        t_start = time.time()
        iteration = 0

        while True:
            elapsed = time.time() - t_start
            if elapsed >= self.scenario.duration_sec:
                break
            if max_iterations and iteration >= max_iterations:
                break

            active = int(len(users) * min(1, elapsed / max(self.scenario.ramp_up_sec, 1)))
            active = max(1, active)

            for u in users[:active]:
                r = u.execute_step()
                r["timestamp"] = datetime.utcnow().isoformat()
                r["elapsed_sec"] = round(elapsed, 2)
                self.results.append(r)

            iteration += 1
            time.sleep(0.1)

        return self.results

    def summary(self):
        if not self.results:
            return {}
        durations = [r["duration_ms"] for r in self.results]
        errors = sum(1 for r in self.results if r["error"])
        return {
            "scenario": self.scenario.name,
            "total_requests": len(self.results),
            "errors": errors,
            "error_rate_pct": round(errors / len(self.results) * 100, 2),
            "avg_ms": round(sum(durations) / len(durations), 2),
            "min_ms": round(min(durations), 2),
            "max_ms": round(max(durations), 2),
        }
