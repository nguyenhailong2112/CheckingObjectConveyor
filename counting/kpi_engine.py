from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class KPIStats:
    total_decisions: int = 0
    total_count_committed: int = 0
    uncertain_count: int = 0
    count_locked: int = 0


class KPIEngine:
    def __init__(self) -> None:
        self.stats = KPIStats()

    def update_from_reason(self, reason: str, count_decision: bool) -> None:
        self.stats.total_decisions += 1
        if count_decision:
            self.stats.total_count_committed += 1
        if reason in {"LOW_CONF", "MOTION_OR_DIRECTION_ANOMALY", "ZONE_ORDER_MISMATCH"}:
            self.stats.uncertain_count += 1
        if reason == "COUNT_LOCKED":
            self.stats.count_locked += 1

    def snapshot(self, fps: float | None = None) -> dict[str, float]:
        total = max(self.stats.total_decisions, 1)
        return {
            "total_decisions": float(self.stats.total_decisions),
            "total_count_committed": float(self.stats.total_count_committed),
            "uncertain_rate": self.stats.uncertain_count / total,
            "count_locked_rate": self.stats.count_locked / total,
            "fps": float(fps or 0.0),
        }