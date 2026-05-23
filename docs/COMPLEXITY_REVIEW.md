# Complexity Review — PoC Core System

Date: 2026-05-23

## 1) Overall conclusion
Current codebase is **not overloaded** for PoC scope. Complexity is mostly structural (module boundaries) rather than algorithmic overhead.

## 2) Where complexity is justified
- Fail-safe counting chain (`uncertain -> reject`, `count lock`) is mandatory for single-count guarantee.
- Geometry validation at config load prevents invalid deployments early.
- Tracking + state-machine + temporal filtering is necessary to avoid frame-wise counting instability.

## 3) Where complexity was unnecessary
- Previous replay runner used camera + pipeline stepping shim to emulate playback.
- For replay regression objective (counting invariants), this introduced extra orchestration complexity without added value.

## 4) Optimization applied in this turn
- Refactored `scripts/replay_runner.py` to a minimal deterministic runner:
  - `ReplayRunner.step(frame)` now directly does `detections -> deterministic track adapter -> counting`.
  - Removed synthetic camera/index rewind shim.
  - Kept behavior stable for regression (`VALIDATED` then `COUNT_LOCKED`).

## 5) Guardrail for next turns
Any new component must satisfy:
1. Direct contribution to count accuracy/stability/fail-safe.
2. Deterministic testability.
3. Lower operational burden than its expected gain.
4. If not, keep it out of core path.