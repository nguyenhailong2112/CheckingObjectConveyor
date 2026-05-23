"""Minimal runtime loop for the M1 system skeleton."""

from __future__ import annotations

from monitoring.structured_logger import StructuredLogger
from runtime.pipeline.stages import CameraStage, CountingStage, DetectionStage, TrackingStage


class PipelineRunner:
    def __init__(
        self,
        camera: CameraStage,
        detector: DetectionStage,
        tracker: TrackingStage,
        counter: CountingStage,
    ) -> None:
        self.camera = camera
        self.detector = detector
        self.tracker = tracker
        self.counter = counter
        self.logger = StructuredLogger(module="pipeline.runner")

    def step(self) -> None:
        packet = self.camera.read()
        if packet is None:
            self.logger.event("camera_empty", severity="WARNING")
            return

        detections = self.detector.run(packet)
        tracks = self.tracker.run(detections, packet)
        decisions = self.counter.run(tracks, timestamp=packet.timestamp)

        self.logger.event(
            "pipeline_step",
            payload={
                "frame_id": packet.frame_id,
                "detections": len(detections),
                "tracks": len(tracks),
                "count_decisions": len(decisions),
            },
        )