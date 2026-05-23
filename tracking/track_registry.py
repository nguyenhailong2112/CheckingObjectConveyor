from __future__ import annotations

from dataclasses import replace

from core.types import TrackState


class TrackRegistry:
    def __init__(self) -> None:
        self._tracks: dict[str, TrackState] = {}

    def upsert(self, track: TrackState) -> TrackState:
        prev = self._tracks.get(track.track_id)
        if prev is None:
            self._tracks[track.track_id] = track
            return track
        merged = replace(
            track,
            counted=prev.counted or track.counted,
            uncertainty=prev.uncertainty or track.uncertainty,
            zone_history=prev.zone_history + track.zone_history,
            age=prev.age + 1,
            missed_frames=0,
            trajectory=prev.trajectory + track.trajectory,
        )
        self._tracks[track.track_id] = merged
        return merged

    def mark_missed(self, active_ids: set[str]) -> None:
        for track_id, track in list(self._tracks.items()):
            if track_id not in active_ids:
                track.missed_frames += 1
                track.age += 1

    def cleanup(self, lost_cleanup: int) -> None:
        for track_id, track in list(self._tracks.items()):
            if track.missed_frames > lost_cleanup:
                self._tracks.pop(track_id, None)

    def items(self) -> list[TrackState]:
        return list(self._tracks.values())