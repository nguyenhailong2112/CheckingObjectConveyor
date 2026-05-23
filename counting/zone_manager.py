from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class RectZone:
    x1: int
    y1: int
    x2: int
    y2: int

    def contains_point(self, x: float, y: float) -> bool:
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2


class ZoneManager:
    def __init__(self, entry_zone: RectZone, verify_zone: RectZone) -> None:
        self.entry_zone = entry_zone
        self.verify_zone = verify_zone

    def in_entry(self, x: float, y: float) -> bool:
        return self.entry_zone.contains_point(x, y)

    def in_verify(self, x: float, y: float) -> bool:
        return self.verify_zone.contains_point(x, y)