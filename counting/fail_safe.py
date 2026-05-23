from __future__ import annotations

from core.types import CountDecision


def reject(reason: str, severity: str = "warning") -> CountDecision:
    return CountDecision(track_id="", count_decision=False, reason=reason, severity=severity)