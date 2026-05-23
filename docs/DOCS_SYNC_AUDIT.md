# DOCS SYNC AUDIT (Final)

Date: 2026-05-23

## Mục tiêu
Xác nhận tài liệu mô tả **đúng với code hiện tại**, không gây hiểu nhầm giữa:
- kiểm tra logic PoC (tests/simulation)
- vận hành runtime thực tế (model + camera/video thật)

## Kết quả rà soát

### 1) README.md
- Đã nêu rõ đây là PoC baseline, chưa production hiện trường.
- Đã tách lệnh test logic và cảnh báo không đại diện runtime production.
- Đã trỏ tới `REAL_RUNTIME_QUICKSTART.md` cho luồng chạy thật.

### 2) UserManual.md
- Đã tách 2 mode: PoC simulation vs Real runtime.
- Đã có checklist điều kiện bắt buộc trước khi gọi là vận hành thực tế.

### 3) OPERATIONS_MANUAL.md
- Đã phân biệt rõ lệnh simulation và điều kiện go-live thực.

### 4) REAL_RUNTIME_QUICKSTART.md
- Đã có lệnh runtime thật với `scripts/run_real_system.py --model ... --source ...`.

### 5) PROJECT_SUMMARY_REPORT.md + FINAL_ACCEPTANCE_AUDIT.md
- Đã nêu giới hạn minh bạch: tracker scaffold, KPI proxy, chưa production-grade full.

### 6) SystemImplementationReport.md
- Đã cập nhật trạng thái hiện tại là M1→M11 hardening waves (không còn dừng ở M1–M3).

## Kết luận
Tài liệu hiện tại đã đồng bộ với codebase:
- Test commands = kiểm tra logic phần mềm.
- Runtime thật = `scripts/run_real_system.py` với model/source thật.
- Không còn dùng tài liệu để diễn giải sai rằng test là vận hành thực tế.