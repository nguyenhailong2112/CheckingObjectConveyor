# Project Kickoff Plan — Industrial Conveyor Object Counting System

## 1) Scope understanding snapshot
This repository currently contains the canonical scope in `ScopeOfWork.md`, defining a fail-safe object counting platform where the core business objective is **Single Count Guarantee**:

- 1 physical object
- 1 persistent identity
- 1 validated crossing
- 1 and only 1 committed count

Primary philosophy:

1. Object existence
2. Object persistence
3. Object validation
4. Single-count guarantee

## 2) Boundary and priorities
### In-scope (PoC / industrial demo)
- Detection
- Tracking
- Counting
- Fail-safe
- Logging + monitoring
- Uncertain-case review queue

### Out-of-scope (PoC)
- OCR / barcode
- Defect inspection
- Classification
- Multi-camera fusion
- MES/ERP/PLC integration
- Cloud analytics

### Priority order
1. Count accuracy
2. Stability
3. Latency
4. Maintainability

## 3) Target KPIs (PoC)
- Count accuracy: >= 99%
- Double count: < 0.2%
- Miss count: < 0.5% (overall scope uses <0.2% in tighter targets; use acceptance gate values for sign-off)
- ID switch: < 1%
- Uncertain rate: < 2%
- FPS: >= 35
- Runtime stability: >= 8h
- Crash: 0

## 4) Phase-1 implementation blueprint (single camera)
### Runtime architecture
Camera -> Queue(maxsize=1) -> ROI -> Adaptive preprocess -> Detection -> Overlap refinement (conditional) -> ByteTrack -> State machine -> Dual-zone validation -> Count lock -> Fail-safe -> KPI/logging/UI

### Core modules
- `runtime/camera`: source, health, reconnect
- `runtime/roi`: ROI + entry/verify zones
- `runtime/preprocess`: adaptive brightness/noise/CLAHE policy
- `vision/detector`: detector + confidence filtering
- `vision/overlap`: candidate analyzer + refinement
- `tracking`: ByteTrack wrapper + temporal + state machine
- `counting`: validation + single-count registry + uncertain rules
- `monitoring`: KPI + health + alerts
- `ui`: operator dashboard (PyQt)
- `data`: review queue + logs + SQLite for PoC

## 5) Non-negotiable logic contracts
1. **No immediate count on raw detection**.
2. Count is only valid when trajectory + direction + zone order are valid.
3. Any uncertainty => no count.
4. One `track_id` can be counted at most once.
5. Camera faults must be isolated/recoverable without full process collapse.

## 6) Implementation principles (must-follow)
1. **Follow ScopeOfWork 100% for PoC**: no feature expansion outside approved scope.
2. **Simple code first**: correct, sufficient, compact, and efficient over over-engineering.
3. **Minimal interfaces, clear contracts**: each module should expose only necessary methods.
4. **Fail-safe before convenience**: uncertain behavior must fail closed (`NO COUNT`).
5. **Checkpoint discipline**: every completed item must be traceable to a checklist row.

## 7) Execution roadmap with checkpoints
Status legend:
- `[DONE]` completed and verified
- `[WIP]` in progress
- `[TODO]` not started
- `[BLOCKED]` waiting dependency

### M0 — Foundation alignment
- [DONE] Read and distill scope into actionable kickoff plan.
- [DONE] Lock business objective and non-negotiable logic contracts.
- [DONE] Define implementation principles (simple, exact, efficient, no bloat).

### M1 — System skeleton (next build target)
- [DONE] Create directory skeleton per scope (`runtime/`, `vision/`, `tracking/`, `counting/`, `monitoring/`, `ui/`, `data/`, `configs/`).
- [DONE] Add base configuration schema (`camera`, `roi`, `preprocess`, `detection`, `tracking`, `counting`, `logging`, `kpi`).
- [DONE] Define core dataclasses: `FramePacket`, `Detection`, `TrackState`, `CountDecision`.
- [DONE] Create structured logger baseline (event, timestamp, module, severity, payload).
- [DONE] Build minimal pluggable pipeline runner (stage interfaces + no-op stubs).
- [DONE] Add queue strategy `maxsize=1` with latest-frame replacement policy.

### M2 — Vision baseline
- [DONE] Integrate detector runtime wrapper and config-driven thresholding.
- [DONE] Add confidence smoothing policy at track level (EMA).
- [DONE] Implement overlap candidate analyzer (area/aspect/density/shape anomaly).
- [DONE] Wire conditional overlap refinement path (enabled only on suspicion).

### M3 — Tracking + persistence
- [DONE] Integrate ByteTrack service wrapper.
- [DONE] Implement track registry and lifecycle fields (`age`, `missed_frames`, `zone_history`, `counted`, `uncertainty`).
- [DONE] Add temporal consistency filter and short-miss recovery.
- [DONE] Implement motion and direction validators.
- [DONE] Implement object state machine (NEW -> ENTERED -> STABLE -> COUNTED/UNCERTAIN/EXITED).

### M4 — Counting integrity + fail-safe
- [DONE] Implement dual-zone manager (ENTRY/VERIFY) and ordered crossing checks.
- [DONE] Implement count commit gate with full validation chain.
- [DONE] Implement count registry lock (one-track-one-count).
- [DONE] Implement uncertain rule engine and severity tagging.
- [DONE] Implement review queue record writer (frame + metadata + history).

### M5 — Operations + KPI
- [DONE] Add KPI engine (count accuracy proxies, uncertain rate, double-count guard metrics, FPS).
- [DONE] Add runtime logs (`count_log`, `uncertain_log`, `system_log`, `error_log`).
- [DONE] Build first operator dashboard skeleton (PyQt: camera panel + KPI panel + event panel + controls).
- [DONE] Add camera health monitor integration (freeze, drop, reconnect, exposure anomaly).

### M6 — Validation + lifecycle readiness
- [DONE] Add test matrix scripts for normal/overlap/blur/dense/occlusion scenarios.
- [DONE] Add long-run harness (4–8h) for stability metrics (FPS drift, memory growth, reconnect success).
- [DONE] Add uncertain sample export structure and metadata format.
- [DONE] Add dataset/model versioning directories and naming rules.
- [DONE] Add retraining trigger checklist and A/B gate template.

## 8) High-precision follow checklist (daily/weekly)
### Daily implementation checklist
- [ ] Confirm today task belongs to in-scope PoC only.
- [ ] Confirm task maps to milestone + checklist item ID.
- [ ] Define acceptance criteria before coding.
- [ ] Implement minimal correct solution (no unnecessary abstraction).
- [ ] Run lint/static/quick run checks.
- [ ] Update checklist status and commit with milestone tag.
- [ ] Record open risks/blockers.

### Weekly engineering checkpoint
- [ ] KPI trend review against targets (accuracy, uncertain, fps, stability).
- [ ] Root-cause review of uncertain/failed cases.
- [ ] Scope compliance review (no drift, no hidden expansion).
- [ ] Performance review (CPU/GPU/RAM/FPS trend).
- [ ] Plan next week by unresolved checklist items only.

## 9) Immediate next coding step
For the next implementation turn, start with **M1** and deliver:

1. Directory skeleton and `config/*.yaml` schema.
2. Core dataclasses (`FramePacket`, `Detection`, `TrackState`, `CountDecision`).
3. Minimal runtime loop with pluggable stage interfaces and structured logs.
4. Checklist tracker file update marking exact `M1` item states.

This allows fast iterative integration while preserving the system design constraints from `ScopeOfWork.md`.

### M7 — Hardening & integration (current phase)
- [DONE] Add pipeline integration test for deterministic detect->track->count flow.
- [DONE] Add config-validation usage in runnable demo entrypoint.
- [DONE] Add strict ROI/zone geometry validator and config sanity bounds.
- [DONE] Add replay runner for deterministic regression packs.


## Documentation sync rule
- [DONE] Every implementation turn must update system operation/report documents to reflect current runnable state.


### M8 — Operational acceptance hardening
- [DONE] Add acceptance gate evaluator for KPI readiness checks.
- [DONE] Add operator health badge in dashboard state/console rendering.
- [DONE] Add event timeline aggregation for operator panel.


### M9 — Final acceptance & handover audit
- [DONE] Execute final full-system audit and publish acceptance report.
- [DONE] Confirm docs synchronized with implemented runtime behavior.


### M10 — Demo handover reliability
- [DONE] Add one-command preflight checker for config + readiness gate + camera health.
- [DONE] Add preflight validation test.


### M11 — Demo execution package
- [DONE] Add one-command demo session runner (preflight + execution + summary).
- [DONE] Add demo session regression test.
- [DONE] Update operations manual with demo execution flow.


### M12 — Real runtime + model lifecycle package
- [DONE] Replace fixed-zone TODO in real runtime with config-driven ENTRY/VERIFY zone membership.
- [DONE] Add lightweight persistent ID association for single-camera tracking baseline.
- [DONE] Add YOLO11m training script with production-oriented defaults and model registry promotion.
- [DONE] Add offline ground-truth count evaluator for Count Accuracy/Miss Count/Double Count.
- [DONE] Add tests for tracker association, tracking-zone-count flow, training config, and evaluator.
- [DONE] Update quickstart/manual/summary/audit docs to reflect current runnable state.
