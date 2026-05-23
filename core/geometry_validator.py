from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Rect:
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1

    @property
    def area(self) -> int:
        return max(self.width, 0) * max(self.height, 0)


class GeometryValidationError(ValueError):
    pass


def _rect_from_list(vals: list[int]) -> Rect:
    if len(vals) != 4:
        raise GeometryValidationError(f"Expected 4 coordinates, got {len(vals)}")
    return Rect(*[int(v) for v in vals])


def validate_roi_and_zones(roi_vals: list[int], entry_vals: list[int], verify_vals: list[int]) -> None:
    roi = _rect_from_list(roi_vals)
    entry = _rect_from_list(entry_vals)
    verify = _rect_from_list(verify_vals)

    for name, rect in (("roi", roi), ("entry_zone", entry), ("verify_zone", verify)):
        if rect.width <= 0 or rect.height <= 0:
            raise GeometryValidationError(f"{name} must have positive width/height")

    if entry.y2 > verify.y1:
        raise GeometryValidationError("entry_zone must be above verify_zone (non-overlapping in Y order)")

    for name, rect in (("entry_zone", entry), ("verify_zone", verify)):
        if rect.x1 < roi.x1 or rect.y1 < roi.y1 or rect.x2 > roi.x2 or rect.y2 > roi.y2:
            raise GeometryValidationError(f"{name} must be fully inside roi")

    if entry.area > roi.area or verify.area > roi.area:
        raise GeometryValidationError("zone area cannot exceed roi area")