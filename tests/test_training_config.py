from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from vision.training.train import TrainingConfig


def run_tests() -> None:
    cfg = TrainingConfig(data="datasets/conveyor/data.yaml", device="0")
    kwargs = cfg.yolo_train_kwargs()
    assert kwargs["data"] == "datasets/conveyor/data.yaml"
    assert kwargs["imgsz"] == 1280
    assert kwargs["optimizer"] == "AdamW"
    assert kwargs["mosaic"] == 0.5
    assert kwargs["mixup"] == 0.1
    assert kwargs["device"] == "0"


if __name__ == "__main__":
    run_tests()
    print("test_training_config: ok")
