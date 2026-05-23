from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DashboardState:
    total_count: int = 0
    uncertain_count: int = 0
    fps: float = 0.0
    camera_status: str = "UNKNOWN"

    def update(self, total_count: int, uncertain_count: int, fps: float, camera_status: str) -> None:
        self.total_count = total_count
        self.uncertain_count = uncertain_count
        self.fps = fps
        self.camera_status = camera_status

    def health_badge(self) -> str:
        if self.camera_status != "HEALTHY":
            return "RED"
        if self.fps < 35:
            return "YELLOW"
        return "GREEN"