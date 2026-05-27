# DOCS SYNC AUDIT (Final)

Date: 2026-05-27

## Mục tiêu
Xác nhận tài liệu mô tả **đúng với code hiện tại**, không gây hiểu nhầm giữa:
- kiểm tra logic PoC (tests/simulation)
- vận hành runtime thực tế (model + camera/video thật)

## Kết quả rà soát

### 1) README.md
- Đã nêu rõ đây là PoC baseline có real single-camera runtime nhưng chưa kèm model/video/GT production.
- Đã tách lệnh test logic và cảnh báo không đại diện runtime production.
- Đã trỏ tới `REAL_RUNTIME_QUICKSTART.md` và `TRAINING_AND_EVALUATION_GUIDE.md`.

### 2) UserManual.md
- Đã tách 2 mode: PoC simulation vs Real runtime.
- Đã bổ sung train detector, real runtime và count evaluation.
- Đã có checklist điều kiện bắt buộc trước khi gọi là vận hành thực tế.

### 3) OPERATIONS_MANUAL.md
- Đã phân biệt rõ lệnh simulation, model lifecycle, real runtime và điều kiện go-live thực.

### 4) REAL_RUNTIME_QUICKSTART.md
- Đã có lệnh runtime thật với `scripts/run_real_system.py --model ... --source ...`.
- Đã bổ sung headless mode, log output, training và evaluator.

### 5) PROJECT_SUMMARY_REPORT.md + FINAL_ACCEPTANCE_AUDIT.md
- Đã nêu giới hạn minh bạch: lightweight tracker, KPI runtime proxy, cần field ground-truth để nghiệm thu.

### 6) SystemImplementationReport.md
- Đã cập nhật trạng thái hiện tại là M1→M12 hardening waves (không còn dừng ở M1–M3).

### 7) TRAINING_AND_EVALUATION_GUIDE.md
- Đã bổ sung tài liệu riêng cho train YOLO, promote model, chạy runtime thật và đánh giá count.

## Kết luận
Tài liệu hiện tại đã đồng bộ với codebase:
- Test commands = kiểm tra logic phần mềm.
- Runtime thật = `scripts/run_real_system.py` với model/source thật.
- Training = `scripts/train_detector.py`.
- Count evaluation = `scripts/evaluate_counts.py`.
- Không còn dùng tài liệu để diễn giải sai rằng test là vận hành thực tế.
