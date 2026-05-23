# OPERATIONS MANUAL

## 1) Phân loại đúng ngữ cảnh vận hành

### 1.1 PoC Logic Run (simulation)
- `python tests/test_suite_runner.py`
- `python scripts/preflight_check.py`
- `python scripts/run_demo_session.py`

Mục đích: kiểm tra logic phần mềm nội bộ.

### 1.2 Real Operation (production)
- Cần camera thật + model thật + dữ liệu thật.
- Repo hiện tại chưa đóng gói sẵn production runtime hoàn chỉnh.

---

## 2) Những lệnh KHÔNG được hiểu sai

Các lệnh tests **không phải** lệnh vận hành hiện trường.
Chúng chỉ là công cụ kiểm tra logic code.

---

## 3) Điều kiện go-live thực tế

- Model inference runtime thật
- Camera pipeline thật
- KPI trên dữ liệu gán nhãn thật
- Chạy ổn định dài giờ theo target


## Runtime thực tế
Xem tài liệu: `REAL_RUNTIME_QUICKSTART.md` để chạy model + camera/video thật.