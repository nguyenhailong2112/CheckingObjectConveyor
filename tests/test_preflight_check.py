from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.preflight_check import run_preflight


def run_tests() -> None:
    out = run_preflight()
    assert out["config_ok"] is True
    assert out["camera_status"] in {"HEALTHY", "WARNING", "ERROR"}
    assert out["acceptance_passed"] is True


if __name__ == "__main__":
    run_tests()
    print("test_preflight_check: ok")