# Model Registry

- `active/`: currently deployed model artifact.
- `archive/`: previous validated versions for rollback.

Training promotion command:
```bash
python scripts/train_detector.py --data datasets/conveyor_v1/data.yaml --name conveyor_yolo11m_v1
```

Runtime default active model:
```text
model_registry/active/best.pt
```

Rollback policy:
If active model degrades KPI, restore last stable model from archive.
