from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AcceptanceThresholds:
    min_fps: float = 35.0
    max_uncertain_rate: float = 0.02
    max_count_locked_rate: float = 0.01


@dataclass(slots=True)
class AcceptanceResult:
    passed: bool
    reasons: list[str]


class AcceptanceGate:
    def __init__(self, thresholds: AcceptanceThresholds | None = None) -> None:
        self.thresholds = thresholds or AcceptanceThresholds()

    def evaluate(self, kpi_snapshot: dict[str, float]) -> AcceptanceResult:
        reasons: list[str] = []
        fps = float(kpi_snapshot.get("fps", 0.0))
        uncertain = float(kpi_snapshot.get("uncertain_rate", 1.0))
        locked = float(kpi_snapshot.get("count_locked_rate", 1.0))

        if fps < self.thresholds.min_fps:
            reasons.append(f"FPS below threshold: {fps:.2f} < {self.thresholds.min_fps:.2f}")
        if uncertain > self.thresholds.max_uncertain_rate:
            reasons.append(
                f"Uncertain rate too high: {uncertain:.4f} > {self.thresholds.max_uncertain_rate:.4f}"
            )
        if locked > self.thresholds.max_count_locked_rate:
            reasons.append(
                f"Count-locked rate too high: {locked:.4f} > {self.thresholds.max_count_locked_rate:.4f}"
            )

        return AcceptanceResult(passed=not reasons, reasons=reasons)