from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.geometry_validator import GeometryValidationError, validate_roi_and_zones


def run_tests() -> None:
    validate_roi_and_zones(
        roi_vals=[150, 200, 1600, 900],
        entry_vals=[200, 300, 1500, 450],
        verify_vals=[200, 650, 1500, 800],
    )

    try:
        validate_roi_and_zones(
            roi_vals=[0, 0, 100, 100],
            entry_vals=[10, 60, 90, 95],
            verify_vals=[10, 50, 90, 90],
        )
        raise AssertionError("Expected GeometryValidationError for bad Y order")
    except GeometryValidationError:
        pass


if __name__ == "__main__":
    run_tests()
    print("test_geometry_validator: ok")