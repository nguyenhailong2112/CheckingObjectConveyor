from __future__ import annotations

from core.types import Detection
from scripts.replay_runner import ReplayFrame, run_replay


def run_tests() -> None:
    frames = [
        ReplayFrame(1, 1.0, [Detection(bbox=(0, 0, 20, 20), confidence=0.95)]),
        ReplayFrame(2, 2.0, [Detection(bbox=(0, 0, 20, 20), confidence=0.95)]),
    ]
    reasons = run_replay(frames)
    assert reasons[0] == "VALIDATED"
    assert reasons[1] == "COUNT_LOCKED"


if __name__ == "__main__":
    run_tests()
    print("test_replay_runner: ok")