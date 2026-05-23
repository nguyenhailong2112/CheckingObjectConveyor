from __future__ import annotations

from dataclasses import dataclass

from core.types import CountDecision, Detection, TrackLifecycle, TrackState
from counting.counting_engine import CountingEngine


@dataclass(slots=True)
class ReplayFrame:
    frame_id: int
    timestamp: float
    detections: list[Detection]


class ReplayTrackerAdapter:
    """Deterministic tracker adapter for regression replay.

    Purposefully simple: for replay regression we validate counting invariants,
    not tracker behavior.
    """

    def run(self, detections: list[Detection]) -> list[TrackState]:
        if not detections:
            return []
        det = detections[0]
        return [
            TrackState(
                track_id="track_fixed_1",
                bbox=det.bbox,
                track_confidence=det.confidence,
                state=TrackLifecycle.STABLE,
                zone_history=["ENTERED", "VERIFY"],
            )
        ]


class ReplayRunner:
    def __init__(self) -> None:
        self.tracker = ReplayTrackerAdapter()
        self.counter = CountingEngine()

    def step(self, frame: ReplayFrame) -> list[CountDecision]:
        tracks = self.tracker.run(frame.detections)
        return self.counter.run(tracks, timestamp=frame.timestamp)


def run_replay(frames: list[ReplayFrame]) -> list[str]:
    runner = ReplayRunner()
    reasons: list[str] = []
    for frame in frames:
        decisions = runner.step(frame)
        reasons.extend([d.reason for d in decisions])
    return reasons


if __name__ == "__main__":
    frames = [
        ReplayFrame(1, 1.0, [Detection(bbox=(0, 0, 20, 20), confidence=0.95)]),
        ReplayFrame(2, 2.0, [Detection(bbox=(0, 0, 20, 20), confidence=0.95)]),
    ]
    out = run_replay(frames)
    print({"reasons": out})