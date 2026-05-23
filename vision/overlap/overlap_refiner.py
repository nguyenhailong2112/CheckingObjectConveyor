"""Conditional overlap refinement path."""

from __future__ import annotations

from typing import Any

from core.types import Detection
from vision.overlap.candidate_analyzer import OverlapCandidateAnalyzer


class ConditionalOverlapRefiner:
    def __init__(self, analyzer: OverlapCandidateAnalyzer, refine_backend: Any) -> None:
        self.analyzer = analyzer
        self.refine_backend = refine_backend

    def run(self, detections: list[Detection], frame: Any, roi_area: int) -> list[Detection]:
        if not self.analyzer.is_overlap_suspected(detections, roi_area=roi_area):
            return detections
        refined = self.refine_backend(frame, detections)
        return refined if refined else detections