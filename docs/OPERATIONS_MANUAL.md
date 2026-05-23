# Operations Manual (Current System Snapshot)

## Purpose
This manual is updated in parallel with implementation and reflects the **current runnable system** in this repository.

## What is implemented now
1. Detect -> Track -> Count pipeline skeleton with fail-safe decisions.
2. One-track-one-count lock and uncertain review export.
3. Config loader with ROI/zone geometry fail-fast validation.
4. Runtime logs, KPI counters, camera health status, operator console text dashboard.
5. Deterministic smoke/integration tests and replay runner baseline.

## Operator quick start
1. Validate config and geometry:
   - `PYTHONPATH=. python tests/test_config_loader.py`
   - `PYTHONPATH=. python tests/test_geometry_validator.py`
2. Verify core counting logic:
   - `PYTHONPATH=. python tests/test_counting_engine.py`
3. Verify pipeline integration:
   - `PYTHONPATH=. python tests/test_pipeline_integration.py`
4. Run demo step:
   - `PYTHONPATH=. python scripts/demo_pipeline.py`
5. Run replay regression:
   - `PYTHONPATH=. python tests/test_replay_runner.py`

## Runtime outputs to monitor
- `logs/count_log.csv`
- `logs/uncertain_log.csv`
- `logs/system_log.csv`
- `logs/error_log.csv`
- `runtime_data/uncertain/*.json`

## Safety principle
If uncertain, do not count. Uncertain cases must be reviewed and retraining decision follows `templates/retraining_gate.md`.


## Event timeline usage
- Operator console now supports recent event timeline (latest 3 by default).
- Typical events: pipeline step, FPS warning, camera reconnect, uncertain case.


## Preflight check
- Run `PYTHONPATH=. python scripts/preflight_check.py` before demo/shift start.
- Expected: `config_ok=True`, `camera_status=HEALTHY`, `acceptance_passed=True`.


## Demo session runner
- Run `PYTHONPATH=. python scripts/run_demo_session.py` for an end-to-end demo flow.
- Flow: preflight -> pipeline steps -> session summary (count/status/last decisions).