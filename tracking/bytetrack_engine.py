from __future__ import annotations

from dataclasses import dataclass

from core.types import Detection, TrackLifecycle, TrackState


@dataclass(slots=True)
class ByteTrackConfig:
    min_box_area: int = 100


class ByteTrackEngine:
    """Simplified ByteTrack-compatible adapter for M3 scaffolding."""

    def __init__(self, config: ByteTrackConfig | None = None) -> None:
        self.config = config or ByteTrackConfig()
        self._next_id = 1

    def update(self, detections: list[Detection]) -> list[TrackState]:
        tracks: list[TrackState] = []
        for det in detections:
            x1, y1, x2, y2 = det.bbox
            if (x2 - x1) * (y2 - y1) < self.config.min_box_area:
                continue
            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0
            tracks.append(
                TrackState(
                    track_id=str(self._next_id),
                    bbox=det.bbox,
                    track_confidence=det.confidence,
                    state=TrackLifecycle.NEW,
                    age=1,
                    trajectory=[(cx, cy)],
                )
            )
            self._next_id += 1
        return tracks