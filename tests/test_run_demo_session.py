from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_demo_session import run_demo_session


def run_tests() -> None:
    s = run_demo_session(steps=3)
    assert s.total_steps == 3
    assert s.total_count >= 1
    assert s.last_camera_status == "HEALTHY"


if __name__ == "__main__":
    run_tests()
    print("test_run_demo_session: ok")