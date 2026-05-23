from __future__ import annotations


class CameraHealthMonitor:
    def __init__(self, expected_fps: float = 40.0, freeze_threshold: int = 120) -> None:
        self.expected_fps = expected_fps
        self.freeze_threshold = freeze_threshold

    def status(self, actual_fps: float, frozen_frames: int, exposure_mean: float) -> str:
        if frozen_frames >= self.freeze_threshold:
            return "ERROR"
        if actual_fps < self.expected_fps * 0.5:
            return "WARNING"
        if exposure_mean < 80 or exposure_mean > 220:
            return "WARNING"
        return "HEALTHY"