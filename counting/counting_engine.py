from __future__ import annotations

from core.types import CountDecision, TrackLifecycle, TrackState
from counting.count_registry import CountRegistry
from counting.uncertain_rules import UncertainRules
from counting.review_queue import ReviewQueueWriter


class CountingEngine:
    def __init__(
        self,
        count_registry: CountRegistry | None = None,
        uncertain_rules: UncertainRules | None = None,
        review_queue: ReviewQueueWriter | None = None,
    ) -> None:
        self.registry = count_registry or CountRegistry()
        self.uncertain_rules = uncertain_rules or UncertainRules()
        self.review_queue = review_queue or ReviewQueueWriter()
        self.total_count = 0

    def evaluate_track(self, track: TrackState, timestamp: float) -> CountDecision:
        uncertain, reason, severity = self.uncertain_rules.evaluate(track)
        if uncertain:
            self.review_queue.write(track, reason=reason, timestamp=timestamp)
            return CountDecision(track_id=track.track_id, count_decision=False, reason=reason, severity=severity)

        if self.registry.has_counted(track.track_id):
            return CountDecision(track_id=track.track_id, count_decision=False, reason="COUNT_LOCKED", severity="info")

        valid_to_count = (
            track.state in (TrackLifecycle.STABLE, TrackLifecycle.COUNTED)
            and "ENTERED" in track.zone_history
            and "VERIFY" in track.zone_history
        )
        if not valid_to_count:
            return CountDecision(track_id=track.track_id, count_decision=False, reason="NOT_READY", severity="info")

        self.registry.lock(track.track_id)
        self.total_count += 1
        return CountDecision(track_id=track.track_id, count_decision=True, reason="VALIDATED", severity="info")

    def run(self, tracks: list[TrackState], timestamp: float) -> list[CountDecision]:
        return [self.evaluate_track(track, timestamp=timestamp) for track in tracks]