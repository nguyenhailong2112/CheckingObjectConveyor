"""Overlap suspicion analyzer based on geometric anomalies."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

from core.types import Detection


@dataclass(slots=True)
class OverlapRules:
    area_ratio_threshold: float = 1.8
    aspect_ratio_threshold: float = 3.0
    density_threshold: float = 0.0008
    shape_change_threshold: float = 0.30
    history_size: int = 30


class OverlapCandidateAnalyzer:
    def __init__(self, rules: OverlapRules | None = None) -> None:
        self.rules = rules or OverlapRules()
        self._area_history: deque[float] = deque(maxlen=self.rules.history_size)
        self._last_aspect: float | None = None

    def is_overlap_suspected(self, detections: list[Detection], roi_area: int) -> bool:
        if not detections:
            return False

        total_area = sum(self._area(det.bbox) for det in detections)
        avg_area = sum(self._area_history) / len(self._area_history) if self._area_history else total_area
        area_ratio = total_area / max(avg_area, 1.0)

        max_aspect = max(self._aspect(det.bbox) for det in detections)
        shape_change = 0.0 if self._last_aspect is None else abs(max_aspect - self._last_aspect) / max(self._last_aspect, 1e-6)
        density = len(detections) / max(roi_area, 1)

        self._area_history.append(total_area)
        self._last_aspect = max_aspect

        return any(
            [
                area_ratio > self.rules.area_ratio_threshold,
                max_aspect > self.rules.aspect_ratio_threshold,
                density > self.rules.density_threshold,
                shape_change > self.rules.shape_change_threshold,
            ]
        )

    @staticmethod
    def _area(bbox: tuple[int, int, int, int]) -> float:
        x1, y1, x2, y2 = bbox
        return max(x2 - x1, 0) * max(y2 - y1, 0)

    @staticmethod
    def _aspect(bbox: tuple[int, int, int, int]) -> float:
        x1, y1, x2, y2 = bbox
        w = max(x2 - x1, 1)
        h = max(y2 - y1, 1)
        return w / h