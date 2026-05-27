from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from monitoring.evaluation.count_evaluator import CountEvaluationThresholds, evaluate_count_logs


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate conveyor count log against ground-truth object rows")
    parser.add_argument("--ground-truth", required=True, help="CSV with one row per true object")
    parser.add_argument("--count-log", default="logs/count_log.csv", help="Runtime count log CSV")
    parser.add_argument("--min-accuracy", type=float, default=0.99)
    parser.add_argument("--max-miss-rate", type=float, default=0.005)
    parser.add_argument("--max-double-rate", type=float, default=0.002)
    args = parser.parse_args()

    result = evaluate_count_logs(
        ground_truth_csv=args.ground_truth,
        count_log_csv=args.count_log,
        thresholds=CountEvaluationThresholds(
            min_count_accuracy=args.min_accuracy,
            max_miss_count_rate=args.max_miss_rate,
            max_double_count_rate=args.max_double_rate,
        ),
    )
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    if not result.passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
