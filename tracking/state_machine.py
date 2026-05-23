from __future__ import annotations

from dataclasses import replace

from core.types import TrackLifecycle, TrackState


class TrackStateMachine:
    def __init__(self, stable_age: int = 5) -> None:
        self.stable_age = stable_age

    def update(self, track: TrackState, in_entry: bool, in_verify: bool) -> TrackState:
        if track.uncertainty:
            return replace(track, state=TrackLifecycle.UNCERTAIN)
        if track.counted:
            return replace(track, state=TrackLifecycle.COUNTED)
        if in_verify and TrackLifecycle.ENTERED.value in track.zone_history:
            return replace(track, state=TrackLifecycle.STABLE)
        if in_entry:
            return replace(track, state=TrackLifecycle.ENTERED)
        if track.age >= self.stable_age:
            return replace(track, state=TrackLifecycle.STABLE)
        return replace(track, state=TrackLifecycle.NEW)