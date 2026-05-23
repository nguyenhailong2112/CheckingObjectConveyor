from __future__ import annotations

from scripts.run_demo_session import run_demo_session


def run_tests() -> None:
    s = run_demo_session(steps=3)
    assert s.total_steps == 3
    assert s.total_count >= 1
    assert s.last_camera_status == "HEALTHY"


if __name__ == "__main__":
    run_tests()
    print("test_run_demo_session: ok")