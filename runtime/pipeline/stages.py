"""Minimal pluggable stage contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from core.types import CountDecision, Detection, FramePacket, TrackState


class CameraStage(Protocol):
    def read(self) -> FramePacket | None: ...


class DetectionStage(Protocol):
    def run(self, packet: FramePacket) -> list[Detection]: ...


class TrackingStage(Protocol):
    def run(self, detections: list[Detection], packet: FramePacket) -> list[TrackState]: ...


class CountingStage(Protocol):
    def run(self, tracks: list[TrackState], timestamp: float) -> list[CountDecision]: ...


@dataclass(slots=True)
class NoOpDetectionStage:
    def run(self, packet: FramePacket) -> list[Detection]:
        return []


@dataclass(slots=True)
class NoOpTrackingStage:
    def run(self, detections: list[Detection], packet: FramePacket) -> list[TrackState]:
        return []


@dataclass(slots=True)
class NoOpCountingStage:
    def run(self, tracks: list[TrackState], timestamp: float) -> list[CountDecision]:
        return []