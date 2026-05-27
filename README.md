# Industrial Conveyor Object Counting PoC

> ⚠️ **Trạng thái hiện tại:** Đây là **PoC core software baseline**, **chưa phải** hệ thống production chạy hiện trường.

Hệ thống theo triết lý:

- 1 vật thể thực
- 1 định danh ổn định
- 1 lần xác thực hợp lệ
- 1 lần đếm duy nhất

---

## 1) Phạm vi hiện tại (đúng sự thật)

Hiện repo đang có:
- Khung pipeline Detect → Track → Count
- Fail-safe counting logic
- Config/ROI validation
- Monitoring + preflight + demo session dạng mô phỏng
- Runtime thật single-camera với YOLO/OpenCV, zone ENTRY/VERIFY từ config, CSV logs
- Training script YOLO + model registry promotion flow
- Offline count evaluator theo ground-truth CSV

Hiện repo **chưa có sẵn**:
- model weights production
- video test thực tế chuẩn nghiệm thu
- benchmark accuracy trên ground-truth hiện trường

---

## 2) Cách chạy đúng ở trạng thái hiện tại

### 2.1 Chạy kiểm tra code logic (không phải vận hành hiện trường)
```bash
python tests/test_suite_runner.py
# hoặc
pytest -q
```

### 2.2 Chạy preflight/demo mô phỏng của PoC
```bash
python scripts/preflight_check.py
python scripts/run_demo_session.py
```

> Hai lệnh trên **không đại diện** cho vận hành production với camera/model thật.

### 2.3 Train model detection
```bash
python scripts/train_detector.py --data datasets/conveyor_v1/data.yaml --name conveyor_yolo11m_v1
```

Xem chi tiết: `docs/TRAINING_AND_EVALUATION_GUIDE.md`.

### 2.4 Chạy runtime thật với model + camera/video
```bash
python scripts/run_real_system.py --model model_registry/active/best.pt --source 0
python scripts/run_real_system.py --model model_registry/active/best.pt --source data/test_video.mp4 --headless
```

### 2.5 Đánh giá count với ground-truth
```bash
python scripts/evaluate_counts.py --ground-truth data/ground_truth.csv --count-log logs/count_log.csv
```

---

## 3) Điều kiện tối thiểu để nghiệm thu thực tế

Repo đã có runtime/script để chạy thật, nhưng nghiệm thu hiện trường vẫn cần dữ liệu ngoài repo:
1. Model weights đã train và promote vào `model_registry/active/best.pt`
2. Camera/video input thật
3. Cấu hình ROI/zone đã calibrate theo line thực tế
4. Ground-truth CSV hoặc biên bản đếm chuẩn để chạy evaluator

Khi đủ 4 điều kiện trên, mới bắt đầu bước “vận hành hiện trường”.

---

## 4) Bộ tài liệu chính

- `UserManual.md` (đã tách rõ mô phỏng vs thực tế)
- `PROJECT_SUMMARY_REPORT.md`
- `FLOWCHART.md`
- `FINAL_ACCEPTANCE_AUDIT.md`
- `TRAINING_AND_EVALUATION_GUIDE.md`


## Runtime thực tế
Xem tài liệu: `REAL_RUNTIME_QUICKSTART.md` để chạy model + camera/video thật.
