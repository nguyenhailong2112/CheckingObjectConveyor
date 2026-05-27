# Training And Evaluation Guide

## 1) Detector Training

Dataset phải theo YOLO format và dùng một class duy nhất:

```yaml
names:
  0: foreground_object
```

Lệnh train baseline theo scope:

```bash
python scripts/train_detector.py --data datasets/conveyor_v1/data.yaml --name conveyor_yolo11m_v1
```

Script dùng cấu hình mặc định:

- `model=yolo11m.pt`
- `imgsz=1280`
- `epochs=100`
- `batch=16`
- `optimizer=AdamW`
- `lr0=0.001`
- `weight_decay=0.0005`
- `patience=20`
- `cos_lr=true`
- `mosaic=0.5`
- `mixup=0.1`

Sau khi train xong, script copy:

- weight version vào `models/<name>.pt`
- active weight vào `model_registry/active/best.pt`
- metrics sidecar vào `models/<name>.metrics.json`

## 2) Real Runtime

Chạy video/camera thật:

```bash
python scripts/run_real_system.py --model model_registry/active/best.pt --source 0
```

Chạy headless để log/benchmark:

```bash
python scripts/run_real_system.py --model model_registry/active/best.pt --source data/test_video.mp4 --headless --max-frames 500
```

Runtime đọc `configs/system.yaml` để lấy ROI, ENTRY zone, VERIFY zone, confidence threshold và KPI threshold.

## 3) Count Evaluation

Chuẩn bị ground-truth CSV với một row cho mỗi vật thể thật đi qua line:

```csv
object_id
obj_0001
obj_0002
```

Đánh giá count log:

```bash
python scripts/evaluate_counts.py --ground-truth data/ground_truth.csv --count-log logs/count_log.csv
```

Acceptance mặc định:

- count accuracy `>=99%`
- miss count `<0.5%`
- double count `<0.2%`

## 4) Retraining Loop

Quy trình đúng:

1. Train baseline.
2. Chạy runtime thật trên video/camera thực tế.
3. Review `runtime_data/uncertain/` và camera-error samples.
4. Bổ sung annotation cho overlap/blur/dense/occlusion.
5. Train version mới.
6. Chỉ promote model nếu evaluator và runtime KPI đều pass.
