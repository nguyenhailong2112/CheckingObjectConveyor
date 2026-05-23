# REAL RUNTIME QUICKSTART (Không phải test giả lập)

## 1) Cài môi trường
```bash
pip install ultralytics opencv-python
```

## 2) Chuẩn bị đầu vào thực tế
- Model weights: ví dụ `models/best.pt`
- Source thật:
  - Webcam: `0`
  - Video file: `data/test_video.mp4`
  - RTSP: `rtsp://...`

## 3) Chạy runtime thật
```bash
python scripts/run_real_system.py --model models/best.pt --source 0
```

Ví dụ chạy video file:
```bash
python scripts/run_real_system.py --model models/best.pt --source data/test_video.mp4
```

Ví dụ chạy RTSP:
```bash
python scripts/run_real_system.py --model models/best.pt --source rtsp://user:pass@ip/stream
```

## 4) Điều khiển
- Nhấn `q` để thoát.
- Cửa sổ hiển thị:
  - bbox detect
  - total count
  - reason gần nhất

## 5) Lưu ý quan trọng
- Đây là runtime thật với model + camera/video thật.
- Các lệnh trong `tests/` chỉ để kiểm tra logic code, không thay thế runtime thật.