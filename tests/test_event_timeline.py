from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from monitoring.event_timeline import EventTimeline


def run_tests() -> None:
    tl = EventTimeline(max_events=3)
    tl.add(1.0, "info", "boot")
    tl.add(2.0, "warning", "fps_drop")
    tl.add(3.0, "error", "camera_lost")
    tl.add(4.0, "info", "camera_recovered")

    latest = tl.latest(3)
    assert len(latest) == 3
    assert latest[0].message == "fps_drop"
    assert latest[-1].message == "camera_recovered"


if __name__ == "__main__":
    run_tests()
    print("test_event_timeline: ok")