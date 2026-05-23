from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.types import TrackLifecycle, TrackState
from counting.counting_engine import CountingEngine


def make_track(
    track_id: str,
    state: TrackLifecycle,
    conf: float = 0.9,
    zone_history: list[str] | None = None,
    uncertainty: bool = False,
) -> TrackState:
    return TrackState(
        track_id=track_id,
        bbox=(0, 0, 10, 10),
        track_confidence=conf,
        state=state,
        zone_history=zone_history or [],
        uncertainty=uncertainty,
    )


def run_tests() -> None:
    engine = CountingEngine()

    t1 = make_track("1", TrackLifecycle.STABLE, zone_history=["ENTERED", "VERIFY"])
    d1 = engine.evaluate_track(t1, timestamp=1.0)
    assert d1.count_decision is True and d1.reason == "VALIDATED"

    d2 = engine.evaluate_track(t1, timestamp=2.0)
    assert d2.count_decision is False and d2.reason == "COUNT_LOCKED"

    t2 = make_track("2", TrackLifecycle.STABLE, conf=0.1, zone_history=["ENTERED", "VERIFY"])
    d3 = engine.evaluate_track(t2, timestamp=3.0)
    assert d3.count_decision is False and d3.reason == "LOW_CONF"

    t3 = make_track("3", TrackLifecycle.STABLE, zone_history=["VERIFY"])
    d4 = engine.evaluate_track(t3, timestamp=4.0)
    assert d4.count_decision is False and d4.reason == "ZONE_ORDER_MISMATCH"

    t4 = make_track("4", TrackLifecycle.NEW, zone_history=["ENTERED"])
    d5 = engine.evaluate_track(t4, timestamp=5.0)
    assert d5.count_decision is False and d5.reason == "NOT_READY"


if __name__ == "__main__":
    run_tests()
    print("test_counting_engine: ok")