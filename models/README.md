# Model Versioning

Use deterministic naming:
- best_v1.pt
- best_v2.pt
- best_v3.pt

Every model version should have a metrics sidecar JSON with:
- precision
- recall
- count_accuracy
- fps

`scripts/train_detector.py` writes:
- `models/<run_name>.pt`
- `models/<run_name>.metrics.json`
- `model_registry/active/best.pt`
