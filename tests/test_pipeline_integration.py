from __future__ import annotations

from core.types import Detection, FramePacket, TrackLifecycle, TrackState
from counting.counting_engine import CountingEngine
from runtime.pipeline.runner import PipelineRunner


class StubCamera:
    def __init__(self) -> None:
        self.frame_id = 0

    def read(self) -> FramePacket:
        self.frame_id += 1
        return FramePacket(frame_id=self.frame_id, timestamp=float(self.frame_id), frame=None)


class StubDetector:
    def run(self, packet: FramePacket) -> list[Detection]:
        return [Detection(bbox=(0, 0, 20, 20), confidence=0.95)]


class StableTrackerAdapter:
    def run(self, detections: list[Detection], packet: FramePacket):
        return [
            TrackState(
                track_id="track_fixed_1",
                bbox=(0, 0, 20, 20),
                track_confidence=0.95,
                state=TrackLifecycle.STABLE,
                zone_history=["ENTERED", "VERIFY"],
            )
        ]


class CountingAdapter:
    def __init__(self) -> None:
        self.engine = CountingEngine()
        self.last_decisions = []

    def run(self, tracks, timestamp: float):
        self.last_decisions = self.engine.run(tracks, timestamp=timestamp)
        return self.last_decisions


def run_tests() -> None:
    counter = CountingAdapter()
    runner = PipelineRunner(
        camera=StubCamera(),
        detector=StubDetector(),
        tracker=StableTrackerAdapter(),
        counter=counter,
    )

    runner.step()
    assert len(counter.last_decisions) == 1
    assert counter.last_decisions[0].count_decision is True
    assert counter.last_decisions[0].reason == "VALIDATED"

    runner.step()
    assert len(counter.last_decisions) == 1
    assert counter.last_decisions[0].count_decision is False
    assert counter.last_decisions[0].reason == "COUNT_LOCKED"


if __name__ == "__main__":
    run_tests()
    print("test_pipeline_integration: ok")