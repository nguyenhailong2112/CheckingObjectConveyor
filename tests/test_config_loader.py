from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.config_loader import load_system_config


def run_tests() -> None:
    cfg = load_system_config("configs/system.yaml")
    assert cfg.detection_confidence_threshold == 0.5


if __name__ == "__main__":
    run_tests()
    print("test_config_loader: ok")