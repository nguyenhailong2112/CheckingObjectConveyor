from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(slots=True)
class CountEvaluationResult:
    ground_truth_count: int
    predicted_count: int
    absolute_error: int
    count_accuracy: float
    miss_count_rate: float
    double_count_rate: float
    passed: bool
    reasons: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(slots=True)
class CountEvaluationThresholds:
    min_count_accuracy: float = 0.99
    max_miss_count_rate: float = 0.005
    max_double_count_rate: float = 0.002


def evaluate_count_logs(
    ground_truth_csv: str,
    count_log_csv: str,
    thresholds: CountEvaluationThresholds | None = None,
) -> CountEvaluationResult:
    thresholds = thresholds or CountEvaluationThresholds()
    gt_count = _count_ground_truth_rows(Path(ground_truth_csv))
    pred_count = _count_committed_predictions(Path(count_log_csv))
    denom = max(gt_count, 1)

    absolute_error = abs(pred_count - gt_count)
    count_accuracy = max(0.0, 1.0 - absolute_error / denom)
    miss_rate = max(gt_count - pred_count, 0) / denom
    double_rate = max(pred_count - gt_count, 0) / denom

    reasons: list[str] = []
    if count_accuracy < thresholds.min_count_accuracy:
        reasons.append(f"Count accuracy below threshold: {count_accuracy:.4f} < {thresholds.min_count_accuracy:.4f}")
    if miss_rate > thresholds.max_miss_count_rate:
        reasons.append(f"Miss count rate too high: {miss_rate:.4f} > {thresholds.max_miss_count_rate:.4f}")
    if double_rate > thresholds.max_double_count_rate:
        reasons.append(f"Double count rate too high: {double_rate:.4f} > {thresholds.max_double_count_rate:.4f}")

    return CountEvaluationResult(
        ground_truth_count=gt_count,
        predicted_count=pred_count,
        absolute_error=absolute_error,
        count_accuracy=count_accuracy,
        miss_count_rate=miss_rate,
        double_count_rate=double_rate,
        passed=not reasons,
        reasons=reasons,
    )


def _count_ground_truth_rows(path: Path) -> int:
    if not path.exists():
        raise FileNotFoundError(f"Ground-truth CSV not found: {path}")
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return sum(1 for _ in reader)


def _count_committed_predictions(path: Path) -> int:
    if not path.exists():
        raise FileNotFoundError(f"Count log CSV not found: {path}")
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "decision" not in (reader.fieldnames or []):
            raise ValueError("Count log must contain a 'decision' column")
        return sum(1 for row in reader if str(row.get("decision", "")).strip() in {"1", "true", "True"})
