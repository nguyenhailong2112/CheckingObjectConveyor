from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.config_loader import load_system_config
from monitoring.acceptance_gate import AcceptanceGate
from monitoring.camera_health import CameraHealthMonitor


def run_preflight() -> dict:
    cfg = load_system_config("configs/system.yaml")

    # Simulated live snapshot baseline for operator go/no-go check.
    snapshot = {
        "fps": 40.0,
        "uncertain_rate": 0.01,
        "count_locked_rate": 0.0,
    }

    gate = AcceptanceGate()
    result = gate.evaluate(snapshot)

    camera_health = CameraHealthMonitor(expected_fps=cfg.raw["camera"]["expected_fps"])
    camera_status = camera_health.status(actual_fps=snapshot["fps"], frozen_frames=0, exposure_mean=120)

    return {
        "config_ok": True,
        "camera_status": camera_status,
        "acceptance_passed": result.passed,
        "acceptance_reasons": result.reasons,
        "snapshot": snapshot,
    }


if __name__ == "__main__":
    output = run_preflight()
    print(output)