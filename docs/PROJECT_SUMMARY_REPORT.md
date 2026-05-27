# BÁO CÁO TỔNG KẾT TOÀN BỘ DỰ ÁN

## 1) Tổng quan

Dự án xây dựng hệ thống PoC đếm vật thể băng tải 1 camera theo triết lý:

- Object Existence
- Object Persistence
- Object Validation
- Single Count Guarantee

Mục tiêu cốt lõi: **đếm đúng 1 lần cho 1 vật thể thực** và ưu tiên fail-safe.

---

## 2) Thành phần đã triển khai

### 2.1 Core
- `core/types.py`: hợp đồng dữ liệu runtime
- `core/config_loader.py`: nạp cấu hình + kiểm tra section bắt buộc
- `core/geometry_validator.py`: kiểm tra ROI/entry/verify fail-fast

### 2.2 Runtime pipeline
- `runtime/pipeline/stages.py`: protocol stage
- `runtime/pipeline/runner.py`: orchestrator tối thiểu
- `runtime/queue/frame_queue.py`: latest-frame queue `maxsize=1`

### 2.3 Vision
- `vision/detector/detector.py`: detector runtime wrapper
- `vision/detector/confidence.py`: EMA confidence
- `vision/overlap/*`: overlap suspicion + conditional refine
- `vision/training/train.py`: script train YOLO11m theo cấu hình scope và promote model

### 2.4 Tracking
- `tracking/bytetrack_engine.py`: lightweight ByteTrack-compatible ID association theo IoU/center
- `tracking/track_registry.py`: quản lý vòng đời track
- `tracking/motion_validator.py`: kiểm tra chuyển động bất thường
- `tracking/state_machine.py`: NEW/ENTERED/STABLE/...
- `tracking/temporal_filter.py`: temporal consistency
- `tracking/tracking_service.py`: tích hợp logic tracking + zone ENTRY/VERIFY từ bbox center

### 2.5 Counting & fail-safe
- `counting/counting_engine.py`: quyết định đếm
- `counting/count_registry.py`: one-track-one-count lock
- `counting/uncertain_rules.py`: luật uncertain
- `counting/review_queue.py`: xuất ca uncertain
- `counting/kpi_engine.py`: chỉ số runtime proxy
- `counting/zone_manager.py`: vùng ENTRY/VERIFY

### 2.6 Monitoring & UI
- `monitoring/acceptance_gate.py`: go/no-go gate
- `monitoring/camera_health.py`: sức khỏe camera
- `monitoring/event_timeline.py`: timeline sự kiện vận hành
- `monitoring/runtime_logs.py`: CSV logs
- `monitoring/evaluation/count_evaluator.py`: offline evaluator theo ground-truth CSV
- `ui/dashboard_state.py`, `ui/operator_console.py`: dashboard console

### 2.7 Scripts vận hành
- `scripts/preflight_check.py`
- `scripts/demo_pipeline.py`
- `scripts/replay_runner.py`
- `scripts/run_demo_session.py`
- `scripts/run_real_system.py`
- `scripts/train_detector.py`
- `scripts/evaluate_counts.py`

### 2.8 Testing
- unit/integration tests trong `tests/`
- regression deterministic: replay + pipeline integration

---

## 3) Kiến trúc hệ thống (sơ đồ)

## 3.1 Sơ đồ tổng thể end-to-end

```text
Camera/Input
   ↓
Preflight + Config Validation
   ↓
Pipeline Runner
   ↓
Detection
   ↓
(Conditional) Overlap Refinement
   ↓
Tracking Service
   ↓
State/Temporal/Motion Validation
   ↓
Counting Engine (Fail-safe)
   ↓
Count Lock + Review Queue
   ↓
KPI/Monitoring/Event Timeline
   ↓
Operator Console + Logs
```

Runtime thật đọc trực tiếp `configs/system.yaml` cho ROI, ENTRY zone, VERIFY zone, confidence threshold và KPI threshold.

## 3.2 Sơ đồ luồng quyết định đếm

```text
Track Input
  ↓
Uncertain Rules?
  ├─ Yes → Reject/Uncertain + Export Review
  └─ No
      ↓
Count Locked?
  ├─ Yes → Reject (COUNT_LOCKED)
  └─ No
      ↓
Zone/State Valid?
  ├─ No → NOT_READY
  └─ Yes
      ↓
Commit Count + Lock Track
```

## 3.3 Sơ đồ tuần tự phiên demo

```text
Operator
  ↓ run_demo_session
Preflight Check
  ↓ pass
Pipeline step loop (N steps)
  ↓
Counting decisions collected
  ↓
Session summary printed
```

---

## 4) Phương pháp triển khai xử lý

1. Thiết kế theo hợp đồng dữ liệu thống nhất giữa stage.
2. Fail-fast ở đầu vào cấu hình (geometry + schema).
3. Fail-safe ở đầu ra quyết định đếm.
4. Deterministic regression cho các logic quan trọng.
5. Tài liệu hóa song song mỗi wave triển khai.

---

## 5) Đánh giá mức độ hoàn thiện hiện tại

### Đã đạt
- PoC runnable end-to-end
- Đầy đủ kiểm định logic cốt lõi
- Có preflight + acceptance + monitoring + docs vận hành
- Có runtime thật single-camera với YOLO/OpenCV, zone thật và CSV logs
- Có training script và model registry promotion flow
- Có offline evaluator cho Count Accuracy/Miss Count/Double Count

### Giới hạn minh bạch
- Tracking hiện là lightweight association, chưa phải ByteTrack production đầy đủ
- UI hiện là console skeleton (chưa PyQt dashboard hoàn chỉnh)
- KPI runtime vẫn là proxy; offline GT evaluator đã có nhưng cần ground-truth thật để nghiệm thu

---

## 6) Hướng cải tiến mở rộng (sau nghiệm thu PoC)

1. Thay lightweight tracker bằng ByteTrack production adapter khi tích hợp line thật.
2. Nâng UI lên dashboard PyQt theo panel công nghiệp.
3. Mở rộng harness 4–8h với telemetry capture đầy đủ.
4. Chuẩn hóa bộ dữ liệu regression từ runtime uncertain samples.
5. A/B model gate có tích hợp số liệu ground-truth thực tế.

---

## 7) Kết luận nghiệm thu kỹ thuật

Hệ thống hiện tại đã hình thành một baseline PoC chỉn chu, đúng scope, có khả năng demo vận hành và có nền tảng tốt để đi vào giai đoạn hardening production.
