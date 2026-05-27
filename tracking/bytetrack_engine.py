from __future__ import annotations

from dataclasses import dataclass

from core.types import Detection, TrackLifecycle, TrackState


@dataclass(slots=True)
class ByteTrackConfig:
    min_box_area: int = 100
    iou_match_threshold: float = 0.30
    max_center_distance: float = 120.0
    max_missed_frames: int = 10


@dataclass(slots=True)
class _ActiveTrack:
    track_id: str
    bbox: tuple[int, int, int, int]
    confidence: float
    age: int = 1
    missed_frames: int = 0


class ByteTrackEngine:
    """Lightweight ByteTrack-compatible tracker contract.

    This is not a full ByteTrack implementation. It preserves stable IDs for
    the single-camera PoC by greedily matching detections to active tracks using
    IoU first and center-distance as a fallback.
    """

    def __init__(self, config: ByteTrackConfig | None = None) -> None:
        self.config = config or ByteTrackConfig()
        self._next_id = 1
        self._active: dict[str, _ActiveTrack] = {}

    def update(self, detections: list[Detection]) -> list[TrackState]:
        valid_detections = [det for det in detections if self._area(det.bbox) >= self.config.min_box_area]
        tracks: list[TrackState] = []
        matched_ids: set[str] = set()

        for det in sorted(valid_detections, key=lambda d: d.confidence, reverse=True):
            track_id = self._match(det, matched_ids)
            if track_id is None:
                track_id = str(self._next_id)
                self._next_id += 1
                active = _ActiveTrack(track_id=track_id, bbox=det.bbox, confidence=det.confidence)
            else:
                previous = self._active[track_id]
                active = _ActiveTrack(
                    track_id=track_id,
                    bbox=det.bbox,
                    confidence=det.confidence,
                    age=previous.age + 1,
                    missed_frames=0,
                )

            self._active[track_id] = active
            matched_ids.add(track_id)
            cx, cy = self._center(det.bbox)
            tracks.append(
                TrackState(
                    track_id=track_id,
                    bbox=det.bbox,
                    track_confidence=det.confidence,
                    state=TrackLifecycle.NEW,
                    age=active.age,
                    missed_frames=active.missed_frames,
                    trajectory=[(cx, cy)],
                )
            )

        self._mark_unmatched_tracks(matched_ids)
        return tracks

    def _match(self, det: Detection, excluded_ids: set[str]) -> str | None:
        best_id: str | None = None
        best_score = -1.0
        det_center = self._center(det.bbox)

        for track_id, track in self._active.items():
            if track_id in excluded_ids:
                continue

            iou = self._iou(det.bbox, track.bbox)
            distance = self._distance(det_center, self._center(track.bbox))
            distance_score = 1.0 - min(distance / max(self.config.max_center_distance, 1.0), 1.0)

            if iou >= self.config.iou_match_threshold:
                score = 2.0 + iou
            elif distance <= self.config.max_center_distance:
                score = distance_score
            else:
                continue

            if score > best_score:
                best_score = score
                best_id = track_id

        return best_id

    def _mark_unmatched_tracks(self, matched_ids: set[str]) -> None:
        for track_id, track in list(self._active.items()):
            if track_id in matched_ids:
                continue
            track.missed_frames += 1
            if track.missed_frames > self.config.max_missed_frames:
                self._active.pop(track_id, None)

    @staticmethod
    def _area(bbox: tuple[int, int, int, int]) -> int:
        x1, y1, x2, y2 = bbox
        return max(x2 - x1, 0) * max(y2 - y1, 0)

    @staticmethod
    def _center(bbox: tuple[int, int, int, int]) -> tuple[float, float]:
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) / 2.0, (y1 + y2) / 2.0)

    @staticmethod
    def _distance(a: tuple[float, float], b: tuple[float, float]) -> float:
        return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

    @staticmethod
    def _iou(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
        ax1, ay1, ax2, ay2 = a
        bx1, by1, bx2, by2 = b
        ix1, iy1 = max(ax1, bx1), max(ay1, by1)
        ix2, iy2 = min(ax2, bx2), min(ay2, by2)
        inter = max(ix2 - ix1, 0) * max(iy2 - iy1, 0)
        union = ByteTrackEngine._area(a) + ByteTrackEngine._area(b) - inter
        return inter / union if union > 0 else 0.0
