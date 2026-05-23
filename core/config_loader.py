from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from core.geometry_validator import validate_roi_and_zones


@dataclass(slots=True)
class SystemConfig:
    raw: dict

    @property
    def detection_confidence_threshold(self) -> float:
        return float(self.raw["detection"]["confidence_threshold"])


REQUIRED_TOP_LEVEL_KEYS = {
    "camera",
    "roi",
    "preprocess",
    "detection",
    "tracking",
    "counting",
    "logging",
    "kpi",
}


def _parse_scalar(value: str):
    v = value.strip()
    if v.lower() in {"true", "false"}:
        return v.lower() == "true"
    if v.startswith("[") and v.endswith("]"):
        items = [i.strip() for i in v[1:-1].split(",") if i.strip()]
        return [_parse_scalar(i) for i in items]
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        return v


def _parse_simple_yaml(text: str) -> dict:
    out: dict = {}
    current: dict | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if not line.startswith("  ") and line.endswith(":"):
            key = line[:-1].strip()
            out[key] = {}
            current = out[key]
            continue
        if line.startswith("  ") and current is not None and ":" in line:
            key, value = line.strip().split(":", 1)
            current[key.strip()] = _parse_scalar(value)
            continue
        raise ValueError(f"Unsupported config line format: {raw_line}")
    return out


def load_system_config(path: str = "configs/system.yaml") -> SystemConfig:
    cfg_path = Path(path)
    data = _parse_simple_yaml(cfg_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("System config must be a mapping")

    missing = REQUIRED_TOP_LEVEL_KEYS - set(data.keys())
    if missing:
        raise ValueError(f"Missing config sections: {sorted(missing)}")

    validate_roi_and_zones(data["roi"]["roi"], data["roi"]["entry_zone"], data["roi"]["verify_zone"])

    return SystemConfig(raw=data)