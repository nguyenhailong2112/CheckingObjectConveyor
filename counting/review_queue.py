from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json

from core.types import TrackState


class ReviewQueueWriter:
    def __init__(self, out_dir: str = "runtime_data/uncertain") -> None:
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def write(self, track: TrackState, reason: str, timestamp: float) -> Path:
        payload = {
            "timestamp": timestamp,
            "track_id": track.track_id,
            "reason": reason,
            "track": asdict(track),
        }
        out = self.out_dir / f"track_{track.track_id}_{int(timestamp * 1000)}.json"
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
        return out