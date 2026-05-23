from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests import (
    test_acceptance_gate,
    test_config_loader,
    test_counting_engine,
    test_event_timeline,
    test_geometry_validator,
    test_pipeline_integration,
    test_preflight_check,
    test_replay_runner,
    test_run_demo_session,
)


def test_all_scripted_checks() -> None:
    test_acceptance_gate.run_tests()
    test_config_loader.run_tests()
    test_counting_engine.run_tests()
    test_event_timeline.run_tests()
    test_geometry_validator.run_tests()
    test_pipeline_integration.run_tests()
    test_preflight_check.run_tests()
    test_replay_runner.run_tests()
    test_run_demo_session.run_tests()