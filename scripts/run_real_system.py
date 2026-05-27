from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.config_loader import load_system_config
from core.types import Detection, FramePacket
from counting.zone_manager import RectZone, ZoneManager
from counting.counting_engine import CountingEngine
from counting.kpi_engine import KPIEngine
from monitoring.acceptance_gate import AcceptanceGate, AcceptanceThresholds
from monitoring.camera_health import CameraHealthMonitor
from monitoring.event_timeline import EventTimeline
from monitoring.runtime_logs import RuntimeCSVLogger
from tracking.bytetrack_engine import ByteTrackConfig
from tracking.tracking_service import TrackingService

try:
    import cv2
except Exception:
    cv2 = None

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None


class OpenCVCamera:
    def __init__(self, source: str | int) -> None:
        if cv2 is None:
            raise RuntimeError("opencv-python is required. Install with: pip install opencv-python")
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open source: {source}")
        self.frame_id = 0
        self.source = source
        self.last_frame_gray = None
        self.frozen_frames = 0

    def read(self) -> FramePacket | None:
        ok, frame = self.cap.read()
        if not ok:
            return None
        self.frame_id += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.last_frame_gray is not None and cv2.absdiff(gray, self.last_frame_gray).mean() < 1.0:
            self.frozen_frames += 1
        else:
            self.frozen_frames = 0
        self.last_frame_gray = gray
        return FramePacket(frame_id=self.frame_id, timestamp=time.time(), frame=frame)

    def exposure_mean(self, frame) -> float:
        return float(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).mean())

    def release(self) -> None:
        self.cap.release()


class YoloDetector:
    def __init__(self, model_path: str, conf: float = 0.5) -> None:
        if YOLO is None:
            raise RuntimeError("ultralytics is not installed. Run: pip install ultralytics")
        self.model = YOLO(model_path)
        self.conf = conf

    def run(self, packet: FramePacket) -> list[Detection]:
        res = self.model(packet.frame, conf=self.conf, iou=0.5, verbose=False)
        out: list[Detection] = []
        for r in res:
            if r.boxes is None:
                continue
            for b in r.boxes:
                xyxy = b.xyxy[0].tolist()
                conf = float(b.conf[0])
                class_id = int(b.cls[0]) if b.cls is not None else 0
                class_name = getattr(r, "names", {}).get(class_id, "foreground_object")
                out.append(
                    Detection(
                        bbox=(int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])),
                        confidence=conf,
                        class_name=str(class_name),
                    )
                )
        return out


class TrackerAdapter:
    def __init__(self, zone_manager: ZoneManager, tracker_config: ByteTrackConfig, lost_cleanup: int) -> None:
        self.tracker = TrackingService(lost_cleanup=lost_cleanup, tracker_config=tracker_config)
        self.zone_manager = zone_manager

    def run(self, detections, packet):
        return self.tracker.run(detections, zone_manager=self.zone_manager)


class CounterAdapter:
    def __init__(self) -> None:
        self.counter = CountingEngine()
        self.last = []

    def run(self, tracks, timestamp: float):
        self.last = self.counter.run(tracks, timestamp=timestamp)
        return self.last



def parse_source(src: str) -> str | int:
    if src.isdigit():
        return int(src)
    return src


def rect_from_config(values: list[int]) -> RectZone:
    return RectZone(x1=int(values[0]), y1=int(values[1]), x2=int(values[2]), y2=int(values[3]))


def draw_zone(view, zone: RectZone, color: tuple[int, int, int], label: str) -> None:
    cv2.rectangle(view, (zone.x1, zone.y1), (zone.x2, zone.y2), color, 2)
    cv2.putText(view, label, (zone.x1, max(zone.y1 - 8, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)


def draw_detection(view, det: Detection) -> None:
    x1, y1, x2, y2 = det.bbox
    cv2.rectangle(view, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(view, f"{det.confidence:.2f}", (x1, max(y1 - 6, 18)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run real detect-track-count pipeline")
    ap.add_argument("--config", default="configs/system.yaml", help="System config path")
    ap.add_argument("--model", required=True, help="Path to model weights, e.g. models/best.pt")
    ap.add_argument("--source", required=True, help="Video path, RTSP URL, or camera index (e.g. 0)")
    ap.add_argument("--conf", type=float, default=None, help="Override detection confidence threshold")
    ap.add_argument("--max-frames", type=int, default=0, help="0 means run until stream ends")
    ap.add_argument("--headless", action="store_true", help="Disable OpenCV preview window")
    ap.add_argument("--log-dir", default="logs", help="Runtime CSV log directory")
    args = ap.parse_args()

    cfg = load_system_config(args.config)
    conf = float(args.conf if args.conf is not None else cfg.raw["detection"]["confidence_threshold"])
    zone_manager = ZoneManager(
        entry_zone=rect_from_config(cfg.raw["roi"]["entry_zone"]),
        verify_zone=rect_from_config(cfg.raw["roi"]["verify_zone"]),
    )
    tracking_cfg = cfg.raw["tracking"]
    tracker_config = ByteTrackConfig(
        min_box_area=int(tracking_cfg["min_box_area"]),
        iou_match_threshold=float(tracking_cfg.get("iou_match_threshold", 0.30)),
        max_center_distance=float(tracking_cfg.get("max_center_distance", 120.0)),
        max_missed_frames=int(tracking_cfg["lost_cleanup"]),
    )

    cam = OpenCVCamera(parse_source(args.source))
    detector = YoloDetector(args.model, conf=conf)
    tracker = TrackerAdapter(
        zone_manager=zone_manager,
        tracker_config=tracker_config,
        lost_cleanup=int(tracking_cfg["lost_cleanup"]),
    )
    counter = CounterAdapter()
    timeline = EventTimeline(max_events=200)
    runtime_logs = RuntimeCSVLogger(log_dir=args.log_dir)
    kpi = KPIEngine()
    camera_health = CameraHealthMonitor(expected_fps=float(cfg.raw["camera"]["expected_fps"]))

    frames = 0
    started = time.time()
    last_status = "UNKNOWN"
    try:
        while True:
            if args.max_frames and frames >= args.max_frames:
                break
            pkt = cam.read()
            if pkt is None:
                break

            detections = detector.run(pkt)
            tracks = tracker.run(detections, pkt)
            decisions = counter.run(tracks, pkt.timestamp)
            for decision in decisions:
                kpi.update_from_reason(decision.reason, decision.count_decision)
                runtime_logs.write_count(pkt.timestamp, decision.track_id, decision.count_decision, decision.reason)
                if decision.severity in {"low", "medium", "high"}:
                    runtime_logs.write_uncertain(pkt.timestamp, decision.track_id, decision.reason, decision.severity)

            view = pkt.frame.copy()
            draw_zone(view, zone_manager.entry_zone, (255, 180, 0), "ENTRY")
            draw_zone(view, zone_manager.verify_zone, (0, 180, 255), "VERIFY")
            for det in detections:
                draw_detection(view, det)
            elapsed = max(time.time() - started, 1e-6)
            fps = frames / elapsed if frames else 0.0
            exposure = cam.exposure_mean(pkt.frame)
            last_status = camera_health.status(actual_fps=fps, frozen_frames=cam.frozen_frames, exposure_mean=exposure)
            cv2.putText(view, f"Count: {counter.counter.total_count}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(view, f"FPS: {fps:.1f} Camera: {last_status}", (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            if decisions:
                cv2.putText(view, f"Last: {decisions[-1].reason}", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            if not args.headless:
                cv2.imshow("Real Conveyor Runtime", view)

            timeline.add(pkt.timestamp, "INFO", f"frame={pkt.frame_id} det={len(detections)} count={counter.counter.total_count}")
            runtime_logs.write_system(pkt.timestamp, "frame", json.dumps({"frame_id": pkt.frame_id, "detections": len(detections), "tracks": len(tracks), "camera_status": last_status}))
            frames += 1

            if not args.headless and cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cam.release()
        if not args.headless:
            cv2.destroyAllWindows()

    elapsed = max(time.time() - started, 1e-6)
    snapshot = kpi.snapshot(fps=frames / elapsed)
    gate = AcceptanceGate(
        AcceptanceThresholds(
            min_fps=float(cfg.raw["kpi"]["target_fps"]),
            max_uncertain_rate=float(cfg.raw["kpi"]["uncertain_rate_max"]),
            max_count_locked_rate=float(cfg.raw["kpi"]["double_count_rate_max"]),
        )
    ).evaluate(snapshot)
    print({
        "frames": frames,
        "total_count": counter.counter.total_count,
        "camera_status": last_status,
        "kpi": snapshot,
        "acceptance_passed": gate.passed,
        "acceptance_reasons": gate.reasons,
        "latest_events": [e.message for e in timeline.latest(5)],
    })
