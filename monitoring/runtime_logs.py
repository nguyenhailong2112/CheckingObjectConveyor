from __future__ import annotations

from pathlib import Path
import csv


class RuntimeCSVLogger:
    def __init__(self, log_dir: str = "logs") -> None:
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._paths = {
            "count": self.log_dir / "count_log.csv",
            "uncertain": self.log_dir / "uncertain_log.csv",
            "system": self.log_dir / "system_log.csv",
            "error": self.log_dir / "error_log.csv",
        }
        self._ensure_headers()

    def _ensure_headers(self) -> None:
        headers = {
            "count": ["timestamp", "track_id", "decision", "reason"],
            "uncertain": ["timestamp", "track_id", "reason", "severity"],
            "system": ["timestamp", "event", "payload"],
            "error": ["timestamp", "error", "payload"],
        }
        for key, path in self._paths.items():
            if path.exists():
                continue
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(headers[key])

    def write_count(self, timestamp: float, track_id: str, decision: bool, reason: str) -> None:
        self._append("count", [timestamp, track_id, int(decision), reason])

    def write_uncertain(self, timestamp: float, track_id: str, reason: str, severity: str) -> None:
        self._append("uncertain", [timestamp, track_id, reason, severity])

    def write_system(self, timestamp: float, event: str, payload: str = "") -> None:
        self._append("system", [timestamp, event, payload])

    def write_error(self, timestamp: float, error: str, payload: str = "") -> None:
        self._append("error", [timestamp, error, payload])

    def _append(self, key: str, row: list[object]) -> None:
        with self._paths[key].open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)