from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import time
from dataclasses import dataclass


@dataclass(slots=True)
class LongRunStats:
    steps: int = 0
    elapsed_sec: float = 0.0


def run_harness(duration_sec: int = 10, step_delay_sec: float = 0.01) -> LongRunStats:
    start = time.time()
    stats = LongRunStats()
    while True:
        now = time.time()
        if now - start >= duration_sec:
            break
        stats.steps += 1
        time.sleep(step_delay_sec)
    stats.elapsed_sec = time.time() - start
    return stats


if __name__ == "__main__":
    s = run_harness()
    print({"steps": s.steps, "elapsed_sec": round(s.elapsed_sec, 3)})