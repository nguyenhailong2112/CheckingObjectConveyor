from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import cv2

from core.types import Detection, FramePacket
from counting.counting_engine import CountingEngine
from monitoring.event_timeline import EventTimeline
from runtime.pipeline.runner import PipelineRunner
from tracking.tracking_service import TrackingService

try:
    from ultralytics import YOLO
except Exception:
    YOLO = None


class OpenCVCamera:
    def __init__(self, source: str | int) -> None:
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open source: {source}")
        self.frame_id = 0

    def read(self) -> FramePacket | None:
        ok, frame = self.cap.read()
        if not ok:
            return None
        self.frame_id += 1
        return FramePacket(frame_id=self.frame_id, timestamp=float(self.frame_id), frame=frame)

    def release(self) -> None:
        self.cap.release()


class YoloDetector:
    def __init__(self, model_path: str, conf: float = 0.5) -> None:
        if YOLO is None:
            raise RuntimeError("ultralytics is not installed. Run: pip install ultralytics")
        self.model = YOLO(model_path)
        self.conf = conf

    def run(self, packet: FramePacket) -> list[Detection]:
        res = self.model(packet.frame, conf=self.conf, verbose=False)
        out: list[Detection] = []
        for r in res:
            if r.boxes is None:
                continue
            for b in r.boxes:
                xyxy = b.xyxy[0].tolist()
                conf = float(b.conf[0])
                out.append(
                    Detection(
                        bbox=(int(xyxy[0]), int(xyxy[1]), int(xyxy[2]), int(xyxy[3])),
                        confidence=conf,
                    )
                )
        return out


class TrackerAdapter:
    def __init__(self) -> None:
        self.tracker = TrackingService()

    def run(self, detections, packet):
        # TODO: replace fixed ids by real zone calculator from bbox center + ZoneManager
        return self.tracker.run(detections, entry_ids={"1"}, verify_ids={"1"})


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


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Run real detect-track-count pipeline")
    ap.add_argument("--model", required=True, help="Path to model weights, e.g. models/best.pt")
    ap.add_argument("--source", required=True, help="Video path, RTSP URL, or camera index (e.g. 0)")
    ap.add_argument("--conf", type=float, default=0.5)
    ap.add_argument("--max-frames", type=int, default=0, help="0 means run until stream ends")
    args = ap.parse_args()

    cam = OpenCVCamera(parse_source(args.source))
    detector = YoloDetector(args.model, conf=args.conf)
    tracker = TrackerAdapter()
    counter = CounterAdapter()
    runner = PipelineRunner(camera=cam, detector=detector, tracker=tracker, counter=counter)
    timeline = EventTimeline(max_events=200)

    frames = 0
    try:
        while True:
            if args.max_frames and frames >= args.max_frames:
                break
            pkt = cam.read()
            if pkt is None:
                break
            # put packet back into runner path by simple adapter: run stages manually for visualization
            detections = detector.run(pkt)
            tracks = tracker.run(detections, pkt)
            decisions = counter.run(tracks, pkt.timestamp)

            view = pkt.frame.copy()
            for det in detections:
                x1, y1, x2, y2 = det.bbox
                cv2.rectangle(view, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(view, f"Count: {counter.counter.total_count}", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            if decisions:
                cv2.putText(view, f"Last: {decisions[0].reason}", (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.imshow("Real Conveyor Runtime", view)

            timeline.add(pkt.timestamp, "INFO", f"frame={pkt.frame_id} det={len(detections)} count={counter.counter.total_count}")
            frames += 1

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()

    print({
        "frames": frames,
        "total_count": counter.counter.total_count,
        "latest_events": [e.message for e in timeline.latest(5)],
    })