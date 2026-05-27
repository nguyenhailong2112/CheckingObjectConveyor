from __future__ import annotations

import csv
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from monitoring.evaluation.count_evaluator import evaluate_count_logs


def run_tests() -> None:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        gt = root / "gt.csv"
        pred = root / "count_log.csv"

        with gt.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["object_id"])
            writer.writerow(["obj_1"])
            writer.writerow(["obj_2"])

        with pred.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "track_id", "decision", "reason"])
            writer.writerow([1.0, "1", 1, "VALIDATED"])
            writer.writerow([2.0, "1", 0, "COUNT_LOCKED"])
            writer.writerow([3.0, "2", 1, "VALIDATED"])

        result = evaluate_count_logs(str(gt), str(pred))
        assert result.ground_truth_count == 2
        assert result.predicted_count == 2
        assert result.count_accuracy == 1.0
        assert result.passed is True


if __name__ == "__main__":
    run_tests()
    print("test_count_evaluator: ok")
