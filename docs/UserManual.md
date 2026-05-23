# HƯỚNG DẪN SỬ DỤNG CHƯƠNG TRÌNH HỆ THỐNG

Tài liệu này dành cho người vận hành (operator) và kỹ sư hiện trường, trình bày theo kiểu **đọc và làm theo**.

---

## 1) Mục tiêu khi vận hành

Bạn cần đảm bảo:
1. Hệ thống sẵn sàng trước ca chạy (preflight pass).
2. Pipeline chạy ổn định trong phiên demo.
3. Theo dõi KPI/cảnh báo và xử lý đúng quy trình fail-safe.

---

## 2) Checklist trước khi chạy (Preflight)

### Bước 1 — Chạy kiểm tra sẵn sàng

```bash
PYTHONPATH=. python scripts/preflight_check.py
```

### Bước 2 — Đánh giá kết quả

Kết quả mong đợi:
- `config_ok = True`
- `camera_status = HEALTHY`
- `acceptance_passed = True`

Nếu `acceptance_passed = False`:
- Xem `acceptance_reasons`
- Không chạy demo chính thức cho đến khi pass

---

## 3) Chạy demo vận hành end-to-end

```bash
PYTHONPATH=. python scripts/run_demo_session.py
```

Ý nghĩa:
- Script tự chạy preflight
- Chạy N bước pipeline demo
- In summary cuối phiên:
  - `total_steps`
  - `total_count`
  - `last_camera_status`
  - `last_decisions`

---

## 4) Theo dõi dashboard console

Thông tin cần nhìn:
- `TOTAL COUNT`
- `UNCERTAIN`
- `FPS`
- `CAMERA`
- `HEALTH BADGE` (`GREEN/YELLOW/RED`)
- `Recent Events`

Nguyên tắc đọc nhanh:
- `HEALTHY + GREEN`: chạy ổn
- `YELLOW`: cần chú ý hiệu năng/cảnh báo
- `RED`: dừng vận hành, kiểm tra camera/config

---

## 5) Quy trình xử lý sự cố nhanh

### Trường hợp A: Camera cảnh báo/lỗi
1. Kiểm tra kết nối camera/stream
2. Chạy lại preflight
3. Chỉ tiếp tục khi trạng thái `HEALTHY`

### Trường hợp B: Uncertain tăng cao
1. Không ép đếm tay
2. Kiểm tra `runtime_data/uncertain/`
3. Review mẫu và đánh giá theo `templates/retraining_gate.md`

### Trường hợp C: Acceptance gate fail
1. Xem `acceptance_reasons`
2. Xử lý nguyên nhân (FPS, uncertain rate, count-locked rate)
3. Chạy lại preflight

---

## 6) Bộ lệnh kiểm định chuẩn trước nghiệm thu phiên chạy

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

## 7) Đầu ra cần lưu trữ sau phiên chạy

- `logs/count_log.csv`
- `logs/uncertain_log.csv`
- `logs/system_log.csv`
- `logs/error_log.csv`
- `runtime_data/uncertain/*.json`

---

## 8) Quy tắc vàng khi vận hành

- **Không chắc chắn thì không đếm**.
- Không bypass fail-safe logic.
- Tài liệu vận hành phải luôn đi cùng phiên bản code hiện tại.