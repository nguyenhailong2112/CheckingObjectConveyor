from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(slots=True)
class EventRecord:
    timestamp: float
    level: str
    message: str


class EventTimeline:
    def __init__(self, max_events: int = 100) -> None:
        self._events: deque[EventRecord] = deque(maxlen=max_events)

    def add(self, timestamp: float, level: str, message: str) -> None:
        self._events.append(EventRecord(timestamp=timestamp, level=level.upper(), message=message))

    def latest(self, n: int = 5) -> list[EventRecord]:
        if n <= 0:
            return []
        return list(self._events)[-n:]