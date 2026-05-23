from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dataclasses import dataclass


@dataclass(slots=True)
class TestCase:
    name: str
    target: str
    status: str = "TODO"


TEST_MATRIX = [
    TestCase("normal", "baseline stability"),
    TestCase("light_overlap", "overlap handling"),
    TestCase("heavy_overlap", "overlap stress"),
    TestCase("blur", "motion blur resilience"),
    TestCase("dense", "dense object scene"),
    TestCase("occlusion", "partial occlusion recovery"),
]


def summary() -> dict[str, int]:
    total = len(TEST_MATRIX)
    done = sum(1 for c in TEST_MATRIX if c.status == "DONE")
    todo = total - done
    return {"total": total, "done": done, "todo": todo}


if __name__ == "__main__":
    print(summary())