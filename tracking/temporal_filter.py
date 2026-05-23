from __future__ import annotations

from dataclasses import replace

from core.types import TrackLifecycle, TrackState


class TemporalConsistencyFilter:
    def __init__(self, min_stable_age: int = 5) -> None:
        self.min_stable_age = min_stable_age

    def apply(self, track: TrackState) -> TrackState:
        if track.uncertainty:
            return track
        if track.age >= self.min_stable_age and track.state == TrackLifecycle.NEW:
            return replace(track, state=TrackLifecycle.STABLE)
        return track