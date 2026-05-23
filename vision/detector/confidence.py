"""Track-level confidence smoothing utilities."""

from __future__ import annotations


class EMAConfidence:
    def __init__(self, alpha: float = 0.7) -> None:
        if not 0.0 < alpha <= 1.0:
            raise ValueError("alpha must be in (0, 1]")
        self.alpha = alpha
        self._state: dict[str, float] = {}

    def update(self, track_id: str, current_confidence: float) -> float:
        prev = self._state.get(track_id)
        if prev is None:
            ema = current_confidence
        else:
            ema = self.alpha * current_confidence + (1 - self.alpha) * prev
        self._state[track_id] = ema
        return ema

    def clear(self, track_id: str) -> None:
        self._state.pop(track_id, None)