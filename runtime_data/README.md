# Runtime Data Layout

This folder stores only selective failure/uncertain samples for retraining and diagnostics.

- uncertain/
- false_positive/
- false_negative/
- overlap_cases/
- camera_errors/

Each sample should include image/frame artifact and `meta.json`.

Example metadata:

```json
{
  "timestamp": "2026-05-23 12:30:22",
  "track_id": "17",
  "reason": "overlap_unresolved",
  "confidence": 0.42,
  "camera": "cam01",
  "bbox": [100, 200, 400, 500]
}
```