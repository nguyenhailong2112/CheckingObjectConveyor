from __future__ import annotations

from core.types import Detection, TrackState
from tracking.bytetrack_engine import ByteTrackEngine
from tracking.motion_validator import MotionValidator
from tracking.state_machine import TrackStateMachine
from tracking.temporal_filter import TemporalConsistencyFilter
from tracking.track_registry import TrackRegistry


class TrackingService:
    def __init__(self, lost_cleanup: int = 10) -> None:
        self.engine = ByteTrackEngine()
        self.registry = TrackRegistry()
        self.motion_validator = MotionValidator()
        self.temporal_filter = TemporalConsistencyFilter()
        self.state_machine = TrackStateMachine()
        self.lost_cleanup = lost_cleanup

    def run(self, detections: list[Detection], entry_ids: set[str] | None = None, verify_ids: set[str] | None = None) -> list[TrackState]:
        entry_ids = entry_ids or set()
        verify_ids = verify_ids or set()

        new_tracks = self.engine.update(detections)
        active_ids: set[str] = set()
        outputs: list[TrackState] = []

        for track in new_tracks:
            active_ids.add(track.track_id)
            track = self.registry.upsert(track)
            track = self.motion_validator.validate(track)

            if track.track_id in entry_ids and (not track.zone_history or track.zone_history[-1] != "ENTERED"):
                track.zone_history.append("ENTERED")
            if track.track_id in verify_ids and (not track.zone_history or track.zone_history[-1] != "VERIFY"):
                track.zone_history.append("VERIFY")

            track = self.state_machine.update(track, track.track_id in entry_ids, track.track_id in verify_ids)
            track = self.temporal_filter.apply(track)
            outputs.append(track)

        self.registry.mark_missed(active_ids)
        self.registry.cleanup(self.lost_cleanup)
        return outputs