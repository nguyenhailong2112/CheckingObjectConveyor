from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.types import Detection
from counting.counting_engine import CountingEngine
from counting.zone_manager import RectZone, ZoneManager
from tracking.tracking_service import TrackingService


def run_tests() -> None:
    tracker = TrackingService()
    counter = CountingEngine()
    zones = ZoneManager(
        entry_zone=RectZone(0, 0, 200, 100),
        verify_zone=RectZone(0, 101, 200, 220),
    )

    tracks_1 = tracker.run([Detection(bbox=(40, 40, 100, 100), confidence=0.95)], zone_manager=zones)
    assert tracks_1[0].zone_history == ["ENTERED"]

    tracks_2 = tracker.run([Detection(bbox=(40, 110, 100, 170), confidence=0.95)], zone_manager=zones)
    assert tracks_2[0].track_id == tracks_1[0].track_id
    assert "ENTERED" in tracks_2[0].zone_history
    assert "VERIFY" in tracks_2[0].zone_history

    decisions = counter.run(tracks_2, timestamp=2.0)
    assert decisions[0].count_decision is True
    assert decisions[0].reason == "VALIDATED"


if __name__ == "__main__":
    run_tests()
    print("test_tracking_zone_count_flow: ok")
