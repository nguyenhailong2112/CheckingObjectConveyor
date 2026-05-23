from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.config_loader import load_system_config
from core.types import FramePacket
from runtime.pipeline.runner import PipelineRunner
from runtime.pipeline.stages import DetectionStage
from tracking.tracking_service import TrackingService
from counting.counting_engine import CountingEngine


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


if __name__ == "__main__":
    cfg = load_system_config("configs/system.yaml")
    assert cfg.detection_confidence_threshold == 0.5

    runner = PipelineRunner(
        camera=StubCamera(),
        detector=StubDetector(),
        tracker=TrackerAdapter(),
        counter=CountingEngine(),
    )
    runner.step()
    print("demo_pipeline: ok")