from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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