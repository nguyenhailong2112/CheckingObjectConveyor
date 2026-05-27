# Dataset Layout

Use one YOLO dataset per field iteration:

```text
datasets/
  conveyor_v1/
    data.yaml
    images/
      train/
      val/
      test/
    labels/
      train/
      val/
      test/
```

Counting scope uses one detector class:

```yaml
names:
  0: foreground_object
```

Keep hard samples from `runtime_data/uncertain/` and camera-error clips as the source for the next retraining version.
