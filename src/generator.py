import random
from src.scenarios import Scenario

class VirtualUser:
    def __init__(self, user_id, scenario):
        self.id = user_id
        self.scenario = scenario

    def pick_step(self):
        weights = [s.weight for s in self.scenario.steps]
        return random.choices(self.scenario.steps, weights=weights, k=1)[0]

    def execute_step(self):
        step = self.pick_step()
        duration = max(0, random.gauss(step.duration_ms, step.duration_ms * 0.3))
        error = random.random() < step.error_rate
        return {
            "user": self.id,
            "step": step.name,
            "duration_ms": round(duration, 2),
            "error": error,
            "think_time": step.think_time_sec,
        }

def generate_users(scenario):
    return [VirtualUser(i, scenario) for i in range(scenario.users)]
