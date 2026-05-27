from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.types import Detection
from tracking.bytetrack_engine import ByteTrackEngine


def run_tests() -> None:
    engine = ByteTrackEngine()

    first = engine.update([Detection(bbox=(10, 10, 50, 50), confidence=0.95)])
    second = engine.update([Detection(bbox=(14, 14, 54, 54), confidence=0.93)])
    assert len(first) == 1
    assert len(second) == 1
    assert first[0].track_id == second[0].track_id
    assert second[0].age == 2

    third = engine.update([Detection(bbox=(300, 300, 340, 340), confidence=0.90)])
    assert third[0].track_id != first[0].track_id

    tiny = engine.update([Detection(bbox=(0, 0, 5, 5), confidence=0.99)])
    assert tiny == []


if __name__ == "__main__":
    run_tests()
    print("test_bytetrack_engine: ok")
