from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dataclasses import dataclass

from core.types import FramePacket
from counting.counting_engine import CountingEngine
from monitoring.camera_health import CameraHealthMonitor
from monitoring.event_timeline import EventTimeline
from runtime.pipeline.runner import PipelineRunner
from runtime.pipeline.stages import DetectionStage
from scripts.preflight_check import run_preflight
from tracking.tracking_service import TrackingService


class StubCamera:
    def __init__(self) -> None:
        self.idx = 0

    def read(self) -> FramePacket:
        self.idx += 1
        return FramePacket(frame_id=self.idx, timestamp=float(self.idx), frame=None)


class StubDetector(DetectionStage):
    def run(self, packet: FramePacket):
        from core.types import Detection

        return [Detection(bbox=(0, 0, 20, 20), confidence=0.9)]


class TrackerAdapter:
    def __init__(self) -> None:
        self.tracker = TrackingService()

    def run(self, detections, packet):
        return self.tracker.run(detections, entry_ids={"1"}, verify_ids={"1"})


@dataclass(slots=True)
class DemoSessionSummary:
    total_steps: int
    total_count: int
    last_camera_status: str
    last_decisions: list[str]


class CountingAdapter:
    def __init__(self) -> None:
        self.engine = CountingEngine()
        self.last_reasons: list[str] = []

    def run(self, tracks, timestamp: float):
        decisions = self.engine.run(tracks, timestamp=timestamp)
        self.last_reasons = [d.reason for d in decisions]
        return decisions



def run_demo_session(steps: int = 5) -> DemoSessionSummary:
    preflight = run_preflight()
    if not preflight["acceptance_passed"]:
        raise RuntimeError(f"Preflight failed: {preflight['acceptance_reasons']}")

    timeline = EventTimeline(max_events=50)
    camera_health = CameraHealthMonitor(expected_fps=40)

    counter = CountingAdapter()
    runner = PipelineRunner(
        camera=StubCamera(),
        detector=StubDetector(),
        tracker=TrackerAdapter(),
        counter=counter,
    )

    for i in range(steps):
        runner.step()
        timeline.add(timestamp=float(i + 1), level="INFO", message=f"step={i+1} reasons={counter.last_reasons}")

    status = camera_health.status(actual_fps=40.0, frozen_frames=0, exposure_mean=120)
    timeline.add(timestamp=float(steps), level="INFO", message=f"camera_status={status}")

    return DemoSessionSummary(
        total_steps=steps,
        total_count=counter.engine.total_count,
        last_camera_status=status,
        last_decisions=counter.last_reasons,
    )


if __name__ == "__main__":
    summary = run_demo_session(steps=5)
    print(summary)