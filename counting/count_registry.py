from __future__ import annotations


class CountRegistry:
    def __init__(self) -> None:
        self._counted_ids: set[str] = set()

    def has_counted(self, track_id: str) -> bool:
        return track_id in self._counted_ids

    def lock(self, track_id: str) -> None:
        self._counted_ids.add(track_id)