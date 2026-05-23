"""Latest-frame queue strategy with maxsize=1."""

from __future__ import annotations

from queue import Empty, Full, Queue

from core.types import FramePacket


class LatestFrameQueue:
    def __init__(self) -> None:
        self._queue: Queue[FramePacket] = Queue(maxsize=1)

    def push(self, packet: FramePacket) -> None:
        if self._queue.full():
            try:
                self._queue.get_nowait()
            except Empty:
                pass
        try:
            self._queue.put_nowait(packet)
        except Full:
            pass

    def pop(self) -> FramePacket | None:
        try:
            return self._queue.get_nowait()
        except Empty:
            return None