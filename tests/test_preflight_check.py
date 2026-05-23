from __future__ import annotations

from scripts.preflight_check import run_preflight


def run_tests() -> None:
    out = run_preflight()
    assert out["config_ok"] is True
    assert out["camera_status"] in {"HEALTHY", "WARNING", "ERROR"}
    assert out["acceptance_passed"] is True


if __name__ == "__main__":
    run_tests()
    print("test_preflight_check: ok")