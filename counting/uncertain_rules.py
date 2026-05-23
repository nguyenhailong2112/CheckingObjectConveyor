from __future__ import annotations

from core.types import TrackState


class UncertainRules:
    def __init__(self, min_track_confidence: float = 0.5) -> None:
        self.min_track_confidence = min_track_confidence

    def evaluate(self, track: TrackState) -> tuple[bool, str, str]:
        if track.track_confidence < self.min_track_confidence:
            return True, "LOW_CONF", "low"
        if track.uncertainty:
            return True, "MOTION_OR_DIRECTION_ANOMALY", "medium"
        if "VERIFY" in track.zone_history and "ENTERED" not in track.zone_history:
            return True, "ZONE_ORDER_MISMATCH", "high"
        return False, "VALID", "info"