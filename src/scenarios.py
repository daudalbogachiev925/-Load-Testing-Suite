from dataclasses import dataclass, field
import yaml
from pathlib import Path

@dataclass
class Step:
    name: str
    weight: int = 1
    think_time_sec: float = 1.0
    duration_ms: float = 100.0
    error_rate: float = 0.01

@dataclass
class Scenario:
    name: str
    description: str
    steps: list
    users: int = 10
    duration_sec: int = 300
    ramp_up_sec: int = 30

    @classmethod
    def from_yaml(cls, path):
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        steps = [Step(**s) for s in data.pop("steps", [])]
        return cls(steps=steps, **data)

    def total_weight(self):
        return sum(s.weight for s in self.steps)

def load_scenarios(folder="scenarios"):
    return [Scenario.from_yaml(p) for p in Path(folder).glob("*.yaml")]
