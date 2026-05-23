from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TrackLifecycle(str, Enum):
    NEW = "NEW"
    ENTERED = "ENTERED"
    STABLE = "STABLE"
    COUNTED = "COUNTED"
    UNCERTAIN = "UNCERTAIN"
    EXITED = "EXITED"


@dataclass(slots=True)
class FramePacket:
    frame_id: int
    timestamp: float
    frame: Any
    camera_status: str = "healthy"


@dataclass(slots=True)
class Detection:
    bbox: tuple[int, int, int, int]
    confidence: float
    class_name: str = "foreground_object"


@dataclass(slots=True)
class TrackState:
    track_id: str
    bbox: tuple[int, int, int, int]
    track_confidence: float
    state: TrackLifecycle
    counted: bool = False
    uncertainty: bool = False
    zone_history: list[str] = field(default_factory=list)
    age: int = 0
    missed_frames: int = 0
    trajectory: list[tuple[float, float]] = field(default_factory=list)


@dataclass(slots=True)
class CountDecision:
    track_id: str
    count_decision: bool
    reason: str
    severity: str = "info"