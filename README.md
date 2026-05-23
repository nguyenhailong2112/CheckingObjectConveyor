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

Hiện repo **chưa có sẵn**:
- model weights production
- camera runtime thật
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

---

## 3) Điều kiện tối thiểu để vận hành thực tế

Bạn phải tích hợp thêm:
1. Model weights + inference runtime thật
2. Camera/video input thật
3. Cấu hình ROI/zone theo line thực tế
4. Bộ KPI evaluator theo dữ liệu ground-truth

Khi đủ 4 điều kiện trên, mới bắt đầu bước “vận hành hiện trường”.

---

## 4) Bộ tài liệu chính

- `UserManual.md` (đã tách rõ mô phỏng vs thực tế)
- `PROJECT_SUMMARY_REPORT.md`
- `FLOWCHART.md`
- `FINAL_ACCEPTANCE_AUDIT.md`


## Runtime thực tế
Xem tài liệu: `REAL_RUNTIME_QUICKSTART.md` để chạy model + camera/video thật.