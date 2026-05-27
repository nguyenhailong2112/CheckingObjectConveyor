from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class TrainingConfig:
    data: str
    model: str = "yolo11m.pt"
    imgsz: int = 1280
    epochs: int = 100
    batch: int = 16
    optimizer: str = "AdamW"
    lr0: float = 0.001
    weight_decay: float = 0.0005
    patience: int = 20
    cos_lr: bool = True
    mosaic: float = 0.5
    mixup: float = 0.1
    workers: int = 8
    seed: int = 42
    device: str | None = None
    project: str = "runs/detect"
    name: str = "conveyor_yolo11m"
    exist_ok: bool = False
    cache: bool = False
    resume: bool = False
    validate: bool = True
    registry_dir: str = "model_registry"
    models_dir: str = "models"

    def yolo_train_kwargs(self) -> dict[str, Any]:
        kwargs: dict[str, Any] = {
            "data": self.data,
            "imgsz": self.imgsz,
            "epochs": self.epochs,
            "batch": self.batch,
            "optimizer": self.optimizer,
            "lr0": self.lr0,
            "weight_decay": self.weight_decay,
            "patience": self.patience,
            "cos_lr": self.cos_lr,
            "mosaic": self.mosaic,
            "mixup": self.mixup,
            "workers": self.workers,
            "seed": self.seed,
            "project": self.project,
            "name": self.name,
            "exist_ok": self.exist_ok,
            "cache": self.cache,
            "resume": self.resume,
        }
        if self.device:
            kwargs["device"] = self.device
        return kwargs


def parse_args() -> TrainingConfig:
    parser = argparse.ArgumentParser(description="Train YOLO detector for conveyor foreground-object counting")
    parser.add_argument("--data", required=True, help="Ultralytics dataset YAML path")
    parser.add_argument("--model", default="yolo11m.pt")
    parser.add_argument("--imgsz", type=int, default=1280)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch", type=int, default=16)
    parser.add_argument("--optimizer", default="AdamW")
    parser.add_argument("--lr0", type=float, default=0.001)
    parser.add_argument("--weight-decay", type=float, default=0.0005)
    parser.add_argument("--patience", type=int, default=20)
    parser.add_argument("--cos-lr", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--mosaic", type=float, default=0.5)
    parser.add_argument("--mixup", type=float, default=0.1)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", default=None)
    parser.add_argument("--project", default="runs/detect")
    parser.add_argument("--name", default="conveyor_yolo11m")
    parser.add_argument("--exist-ok", action="store_true")
    parser.add_argument("--cache", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--no-validate", action="store_true")
    parser.add_argument("--registry-dir", default="model_registry")
    parser.add_argument("--models-dir", default="models")
    args = parser.parse_args()
    return TrainingConfig(
        data=args.data,
        model=args.model,
        imgsz=args.imgsz,
        epochs=args.epochs,
        batch=args.batch,
        optimizer=args.optimizer,
        lr0=args.lr0,
        weight_decay=args.weight_decay,
        patience=args.patience,
        cos_lr=args.cos_lr,
        mosaic=args.mosaic,
        mixup=args.mixup,
        workers=args.workers,
        seed=args.seed,
        device=args.device,
        project=args.project,
        name=args.name,
        exist_ok=args.exist_ok,
        cache=args.cache,
        resume=args.resume,
        validate=not args.no_validate,
        registry_dir=args.registry_dir,
        models_dir=args.models_dir,
    )


def train_detector(config: TrainingConfig) -> dict[str, Any]:
    data_path = Path(config.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset YAML not found: {data_path}")

    try:
        from ultralytics import YOLO
    except Exception as exc:
        raise RuntimeError("ultralytics is required. Install with: pip install ultralytics") from exc

    model = YOLO(config.model)
    train_result = model.train(**config.yolo_train_kwargs())
    metrics = model.val() if config.validate else None

    trainer = getattr(model, "trainer", None)
    run_dir = Path(getattr(train_result, "save_dir", None) or getattr(trainer, "save_dir", Path(config.project) / config.name))
    weights_dir = run_dir / "weights"
    best_weight = weights_dir / "best.pt"
    if not best_weight.exists():
        raise FileNotFoundError(f"Expected trained weight not found: {best_weight}")

    version_name = run_dir.name
    models_dir = Path(config.models_dir)
    registry_active = Path(config.registry_dir) / "active"
    registry_archive = Path(config.registry_dir) / "archive"
    models_dir.mkdir(parents=True, exist_ok=True)
    registry_active.mkdir(parents=True, exist_ok=True)
    registry_archive.mkdir(parents=True, exist_ok=True)

    version_weight = models_dir / f"{version_name}.pt"
    active_weight = registry_active / "best.pt"
    if active_weight.exists():
        archived = registry_archive / f"best_{int(active_weight.stat().st_mtime)}.pt"
        shutil.copy2(active_weight, archived)
    shutil.copy2(best_weight, version_weight)
    shutil.copy2(best_weight, active_weight)

    summary = {
        "config": asdict(config),
        "run_dir": str(run_dir),
        "source_weight": str(best_weight),
        "version_weight": str(version_weight),
        "active_weight": str(active_weight),
        "train_result": _safe_result_dict(train_result),
        "validation": _safe_result_dict(metrics),
    }
    metrics_path = models_dir / f"{version_name}.metrics.json"
    metrics_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary


def _safe_result_dict(result: Any) -> dict[str, Any] | None:
    if result is None:
        return None
    out: dict[str, Any] = {}
    for attr in ("fitness", "speed", "results_dict", "box"):
        value = getattr(result, attr, None)
        if value is None:
            continue
        try:
            json.dumps(value)
            out[attr] = value
        except TypeError:
            out[attr] = str(value)
    return out


def main() -> None:
    summary = train_detector(parse_args())
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
