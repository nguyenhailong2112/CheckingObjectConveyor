from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from monitoring.acceptance_gate import AcceptanceGate


def run_tests() -> None:
    gate = AcceptanceGate()

    good = gate.evaluate({"fps": 40.0, "uncertain_rate": 0.01, "count_locked_rate": 0.0})
    assert good.passed is True
    assert len(good.reasons) == 0

    bad = gate.evaluate({"fps": 20.0, "uncertain_rate": 0.10, "count_locked_rate": 0.02})
    assert bad.passed is False
    assert len(bad.reasons) == 3


if __name__ == "__main__":
    run_tests()
    print("test_acceptance_gate: ok")