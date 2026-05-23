"""Config-driven detector runtime wrapper (M2 baseline)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.types import Detection, FramePacket


@dataclass(slots=True)
class DetectorConfig:
    confidence_threshold: float = 0.5


class DetectorRuntime:
    """Thin adapter around detector backend output.

    Backend callable must return iterable of dict items with keys:
    `bbox` (x1,y1,x2,y2) and `confidence`.
    """

    def __init__(self, config: DetectorConfig, backend: Any) -> None:
        self.config = config
        self.backend = backend

    def run(self, packet: FramePacket) -> list[Detection]:
        raw = self.backend(packet.frame)
        results: list[Detection] = []
        for item in raw:
            conf = float(item.get("confidence", 0.0))
            if conf < self.config.confidence_threshold:
                continue
            bbox = tuple(item["bbox"])
            results.append(Detection(bbox=bbox, confidence=conf))
        return results