# Industrial Conveyor Object Counting PoC

Hệ thống PoC đếm vật thể trên băng tải theo triết lý **fail-safe** và **Single Count Guarantee**:

> 1 vật thể vật lý thực → 1 định danh ổn định → 1 lần xác thực hợp lệ → 1 lần đếm duy nhất.

---

## 1) Mục tiêu dự án

- Xây dựng pipeline **Detect → Track → Count** ổn định cho bài toán băng tải 1 camera.
- Ưu tiên theo thứ tự:
  1. Độ chính xác đếm
  2. Tính ổn định
  3. Độ trễ
  4. Dễ bảo trì
- Áp dụng nguyên tắc: **Không chắc chắn thì không đếm**.

---

## 2) Trạng thái hiện tại

Hệ thống đã có đầy đủ baseline PoC:

- Core runtime contracts + config validation
- Tracking lifecycle + temporal consistency
- Counting fail-safe + one-track-one-count lock
- Monitoring/KPI/acceptance gate + event timeline
- Preflight checker + demo session runner + replay regression
- Bộ tài liệu vận hành, báo cáo tổng kết, audit nghiệm thu

---

## 3) Tài liệu chính

1. **Hướng dẫn sử dụng vận hành:** `UserManual.md`
2. **Báo cáo tổng kết kỹ thuật:** `PROJECT_SUMMARY_REPORT.md`
3. **Audit nghiệm thu cuối:** `FINAL_ACCEPTANCE_AUDIT.md`
4. **Sổ tay vận hành nhanh:** `OPERATIONS_MANUAL.md`

---

## 4) Chạy nhanh

### 4.1. Preflight trước demo

```bash
PYTHONPATH=. python scripts/preflight_check.py
```

### 4.2. Chạy demo session end-to-end

```bash
PYTHONPATH=. python scripts/run_demo_session.py
```

### 4.3. Chạy regression test cốt lõi

```bash
PYTHONPATH=. python tests/test_config_loader.py
PYTHONPATH=. python tests/test_geometry_validator.py
PYTHONPATH=. python tests/test_counting_engine.py
PYTHONPATH=. python tests/test_pipeline_integration.py
PYTHONPATH=. python tests/test_replay_runner.py
PYTHONPATH=. python tests/test_acceptance_gate.py
PYTHONPATH=. python tests/test_event_timeline.py
PYTHONPATH=. python tests/test_preflight_check.py
PYTHONPATH=. python tests/test_run_demo_session.py
```

---

## 5) Cấu trúc thư mục nổi bật

- `core/`: kiểu dữ liệu, config loader, validator hình học
- `runtime/`: pipeline runner, stage contracts, queue chiến lược latest-frame
- `vision/`: detector wrapper, EMA confidence, overlap analyzer/refiner
- `tracking/`: tracking service + state machine + temporal filter
- `counting/`: fail-safe counting engine + uncertain rules + count lock
- `monitoring/`: KPI gate, camera health, event timeline, runtime logs
- `ui/`: console dashboard state và operator view
- `scripts/`: preflight/demo/replay tools
- `tests/`: unit + integration + harness

---

## 6) Lưu ý

Đây là **PoC baseline đã sẵn sàng demo**. Để production hóa, cần tiếp tục:

- Tích hợp tracker/detector runtime production thật
- Bổ sung UI PyQt đầy đủ
- Mở rộng kiểm thử tải dài giờ theo dữ liệu thực tế