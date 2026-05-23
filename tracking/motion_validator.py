from __future__ import annotations

from dataclasses import replace

from core.types import TrackState


class MotionValidator:
    def __init__(self, max_pixel_speed: float = 250.0, direction: str = "top_to_bottom") -> None:
        self.max_pixel_speed = max_pixel_speed
        self.direction = direction

    def validate(self, track: TrackState) -> TrackState:
        if len(track.trajectory) < 2:
            return track
        (x1, y1), (x2, y2) = track.trajectory[-2], track.trajectory[-1]
        speed = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        reverse = self.direction == "top_to_bottom" and (y2 - y1) < 0

        if speed > self.max_pixel_speed or reverse:
            return replace(track, uncertainty=True)
        return track