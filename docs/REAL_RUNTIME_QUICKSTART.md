# REAL RUNTIME QUICKSTART (Không phải test giả lập)

## 1) Cài môi trường
```bash
pip install -r requirements.txt
```

## 2) Chuẩn bị đầu vào thực tế
- Model weights: ví dụ `model_registry/active/best.pt`
- Source thật:
  - Webcam: `0`
  - Video file: `data/test_video.mp4`
  - RTSP: `rtsp://...`
- ROI/ENTRY/VERIFY zone trong `configs/system.yaml`

## 3) Chạy runtime thật
```bash
python scripts/run_real_system.py --model model_registry/active/best.pt --source 0
```

Ví dụ chạy video file:
```bash
python scripts/run_real_system.py --model model_registry/active/best.pt --source data/test_video.mp4
```

Ví dụ chạy RTSP:
```bash
python scripts/run_real_system.py --model model_registry/active/best.pt --source rtsp://user:pass@ip/stream
```

Ví dụ benchmark/log không mở cửa sổ:
```bash
python scripts/run_real_system.py --model model_registry/active/best.pt --source data/test_video.mp4 --headless --max-frames 500
```

## 4) Điều khiển
- Nhấn `q` để thoát.
- Cửa sổ hiển thị:
  - bbox detect
  - ENTRY/VERIFY zone
  - total count
  - FPS/camera status
  - reason gần nhất

Runtime ghi CSV log vào `logs/`:
- `count_log.csv`
- `uncertain_log.csv`
- `system_log.csv`
- `error_log.csv`

## 5) Train model trước khi chạy thật
```bash
python scripts/train_detector.py --data datasets/conveyor_v1/data.yaml --name conveyor_yolo11m_v1
```

Sau khi train, active model nằm ở:
```text
model_registry/active/best.pt
```

## 6) Đánh giá count sau phiên chạy
```bash
python scripts/evaluate_counts.py --ground-truth data/ground_truth.csv --count-log logs/count_log.csv
```

## 7) Lưu ý quan trọng
- Đây là runtime thật với model + camera/video thật.
- Các lệnh trong `tests/` chỉ để kiểm tra logic code, không thay thế runtime thật.
