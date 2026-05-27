# OPERATIONS MANUAL

## 1) Phân loại đúng ngữ cảnh vận hành

### 1.1 PoC Logic Run (simulation)
- `python tests/test_suite_runner.py`
- `python scripts/preflight_check.py`
- `python scripts/run_demo_session.py`

Mục đích: kiểm tra logic phần mềm nội bộ.

### 1.2 Real Operation (production)
- Cần camera thật + model thật + dữ liệu thật.
- Repo hiện tại đã có single-camera runtime với YOLO/OpenCV, zone từ config, CSV logs và KPI snapshot.
- Chạy: `python scripts/run_real_system.py --model model_registry/active/best.pt --source 0`

### 1.3 Model lifecycle
- Train: `python scripts/train_detector.py --data datasets/conveyor_v1/data.yaml --name conveyor_yolo11m_v1`
- Active model: `model_registry/active/best.pt`
- Offline count evaluation: `python scripts/evaluate_counts.py --ground-truth data/ground_truth.csv --count-log logs/count_log.csv`

---

## 2) Những lệnh KHÔNG được hiểu sai

Các lệnh tests **không phải** lệnh vận hành hiện trường.
Chúng chỉ là công cụ kiểm tra logic code.

---

## 3) Điều kiện go-live thực tế

- Model đã train/promote
- Camera/video source thật
- ROI/ENTRY/VERIFY zone đã calibrate
- KPI trên dữ liệu gán nhãn thật
- Chạy ổn định dài giờ theo target


## Runtime thực tế
Xem tài liệu: `REAL_RUNTIME_QUICKSTART.md` để chạy model + camera/video thật.
