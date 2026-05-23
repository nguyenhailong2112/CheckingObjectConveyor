# FLOWCHART — Kiến trúc & Luồng xử lý hệ thống (Mermaid)

Tài liệu này tổng hợp đầy đủ các sơ đồ kỹ thuật quan trọng nhất của hệ thống PoC đếm vật thể băng tải.

---

## 1) Kiến trúc tổng thể hệ thống (Logical Architecture)

```mermaid
flowchart TD
    A[Camera/Input Source] --> B[Config Loader + Geometry Validator]
    B --> C[Runtime Pipeline Runner]

    C --> D[Detection Stage]
    D --> E[Overlap Candidate Analyzer]
    E -->|Không nghi ngờ overlap| F[Tracking Service]
    E -->|Nghi ngờ overlap| G[Conditional Overlap Refiner]
    G --> F

    F --> H[State Machine + Temporal Filter + Motion Validator]
    H --> I[Counting Engine]

    I --> J[Count Registry Lock]
    I --> K[Uncertain Rules]
    K -->|Uncertain| L[Review Queue Export]

    I --> M[KPI Engine]
    M --> N[Acceptance Gate]

    C --> O[Structured Logger]
    I --> P[Runtime CSV Logs]
    M --> Q[Operator Console + Event Timeline]

    N --> Q
    L --> R[runtime_data/uncertain]
```

---

## 2) Kiến trúc module theo package

```mermaid
flowchart LR
    subgraph CORE[core/]
        C1[types.py]
        C2[config_loader.py]
        C3[geometry_validator.py]
    end

    subgraph RUNTIME[runtime/]
        R1[pipeline/stages.py]
        R2[pipeline/runner.py]
        R3[queue/frame_queue.py]
    end

    subgraph VISION[vision/]
        V1[detector/detector.py]
        V2[detector/confidence.py]
        V3[overlap/candidate_analyzer.py]
        V4[overlap/overlap_refiner.py]
    end

    subgraph TRACKING[tracking/]
        T1[bytetrack_engine.py]
        T2[track_registry.py]
        T3[state_machine.py]
        T4[motion_validator.py]
        T5[temporal_filter.py]
        T6[tracking_service.py]
    end

    subgraph COUNTING[counting/]
        K1[counting_engine.py]
        K2[count_registry.py]
        K3[uncertain_rules.py]
        K4[review_queue.py]
        K5[kpi_engine.py]
        K6[zone_manager.py]
    end

    subgraph MONITORING[monitoring/]
        M1[structured_logger.py]
        M2[runtime_logs.py]
        M3[camera_health.py]
        M4[acceptance_gate.py]
        M5[event_timeline.py]
    end

    subgraph UI[ui/]
        U1[dashboard_state.py]
        U2[operator_console.py]
    end

    C1 --> R1
    C2 --> R2
    C3 --> C2

    R2 --> V1
    V1 --> V3
    V3 --> V4
    V4 --> T6

    T6 --> K1
    K1 --> K2
    K1 --> K3
    K3 --> K4
    K1 --> K5

    K5 --> M4
    R2 --> M1
    K1 --> M2
    M3 --> U1
    M4 --> U1
    M5 --> U2
    U1 --> U2
```

---

## 3) Luồng end-to-end runtime (mỗi frame)

```mermaid
flowchart TD
    S0[Frame đến từ camera] --> S1[Queue latest-frame maxsize=1]
    S1 --> S2[PipelineRunner.step]
    S2 --> S3[Detection]
    S3 --> S4[Overlap suspicion check]
    S4 -->|No| S5[Giữ detection gốc]
    S4 -->|Yes| S6[Refine overlap]
    S5 --> S7[TrackingService.run]
    S6 --> S7

    S7 --> S8[Registry upsert + missed-frame update]
    S8 --> S9[Motion validation]
    S9 --> S10[State machine update]
    S10 --> S11[Temporal consistency filter]

    S11 --> S12[CountingEngine.evaluate_track]
    S12 --> S13{Uncertain?}
    S13 -->|Yes| S14[Reject + review_queue.write]
    S13 -->|No| S15{Count locked?}
    S15 -->|Yes| S16[Reject COUNT_LOCKED]
    S15 -->|No| S17{Zone/State hợp lệ?}
    S17 -->|No| S18[NOT_READY]
    S17 -->|Yes| S19[Commit count + lock track]

    S14 --> S20[KPI update + logs + timeline]
    S16 --> S20
    S18 --> S20
    S19 --> S20
```

---

## 4) Luồng thuật toán CountingEngine (chi tiết quyết định)

```mermaid
flowchart TD
    A[Input: TrackState + timestamp] --> B[Evaluate uncertain_rules]
    B --> C{uncertain?}
    C -->|Yes| D[Write review sample]
    D --> E[Return CountDecision=False + reason]

    C -->|No| F{track_id đã locked?}
    F -->|Yes| G[Return COUNT_LOCKED]

    F -->|No| H{state in STABLE/COUNTED?}
    H -->|No| I[Return NOT_READY]

    H -->|Yes| J{zone_history có ENTERED + VERIFY?}
    J -->|No| I
    J -->|Yes| K[registry.lock(track_id)]
    K --> L[total_count += 1]
    L --> M[Return VALIDATED]
```

---

## 5) State machine vòng đời track

```mermaid
stateDiagram-v2
    [*] --> NEW
    NEW --> ENTERED: in_entry
    ENTERED --> STABLE: age>=threshold hoặc verify hợp lệ
    STABLE --> COUNTED: counted=True
    NEW --> UNCERTAIN: uncertainty=True
    ENTERED --> UNCERTAIN: uncertainty=True
    STABLE --> UNCERTAIN: uncertainty=True
    COUNTED --> EXITED: out_of_roi/cleanup
    UNCERTAIN --> EXITED: cleanup
```

---

## 6) Sequence diagram — preflight + demo session runner

```mermaid
sequenceDiagram
    participant OP as Operator
    participant DF as run_demo_session.py
    participant PF as preflight_check.py
    participant CFG as config_loader
    participant AG as acceptance_gate
    participant PR as PipelineRunner
    participant TR as TrackingService
    participant CE as CountingEngine

    OP->>DF: Start demo session
    DF->>PF: run_preflight()
    PF->>CFG: load_system_config()
    CFG-->>PF: config_ok
    PF->>AG: evaluate(snapshot)
    AG-->>PF: pass/fail + reasons
    PF-->>DF: preflight result

    alt preflight fail
        DF-->>OP: Stop + reasons
    else preflight pass
        loop each step
            DF->>PR: step()
            PR->>TR: run(detections,...)
            TR-->>PR: tracks
            PR->>CE: run(tracks, timestamp)
            CE-->>PR: decisions
        end
        DF-->>OP: DemoSessionSummary
    end
```

---

## 7) Sequence diagram — replay regression

```mermaid
sequenceDiagram
    participant TEST as test_replay_runner
    participant RR as replay_runner
    participant RT as ReplayTrackerAdapter
    participant CE as CountingEngine

    TEST->>RR: run_replay(frames)
    loop frame in frames
        RR->>RT: run(detections)
        RT-->>RR: deterministic tracks
        RR->>CE: run(tracks, timestamp)
        CE-->>RR: decisions/reasons
    end
    RR-->>TEST: reasons list
    TEST->>TEST: assert VALIDATED -> COUNT_LOCKED
```

---

## 8) Luồng Acceptance Gate (go/no-go)

```mermaid
flowchart TD
    A[KPI snapshot] --> B[Check FPS >= min_fps]
    B --> C[Check uncertain_rate <= max_uncertain_rate]
    C --> D[Check count_locked_rate <= max_count_locked_rate]
    D --> E{Any violation?}
    E -->|Yes| F[passed=False + reasons]
    E -->|No| G[passed=True]
```

---

## 9) Luồng Event Timeline cho operator

```mermaid
flowchart LR
    A[Runtime event] --> B[event_timeline.add]
    B --> C[deque max_events]
    C --> D[latest(n)]
    D --> E[OperatorConsole.render_text]
```

---

## 10) Luồng dữ liệu vận hành và hậu kiểm

```mermaid
flowchart TD
    A[Counting decisions] --> B[logs/count_log.csv]
    A --> C[logs/uncertain_log.csv]
    A --> D[logs/system_log.csv]

    E[Uncertain case] --> F[review_queue.write]
    F --> G[runtime_data/uncertain/*.json]

    G --> H[Human review]
    H --> I[Dataset update]
    I --> J[Retraining gate template]
```

---

## 11) Sơ đồ cây vận hành nhanh cho operator

```mermaid
flowchart TD
    A[Start ca chạy] --> B[Run preflight_check]
    B --> C{acceptance_passed?}
    C -->|No| D[Fix issues theo acceptance_reasons]
    D --> B
    C -->|Yes| E[Run demo_session hoặc runtime chính]
    E --> F[Theo dõi dashboard + event timeline]
    F --> G{Uncertain tăng cao?}
    G -->|Yes| H[Review runtime_data/uncertain + đánh giá retrain]
    G -->|No| I[Tiếp tục vận hành]
    I --> J[End ca + lưu logs]
    H --> J
```

---

## 12) Ghi chú kỹ thuật quan trọng

- Các sơ đồ phản ánh **trạng thái code hiện tại** trong repo.
- Đây là baseline PoC; các node production-level (tracker backend thật, UI PyQt đầy đủ, GT evaluator đầy đủ) là bước tiếp theo.
- Nguyên tắc bất biến: **Không chắc chắn thì không đếm**.