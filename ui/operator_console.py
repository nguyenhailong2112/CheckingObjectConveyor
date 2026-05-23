from __future__ import annotations

from monitoring.event_timeline import EventTimeline
from ui.dashboard_state import DashboardState


class OperatorConsole:
    """Console-first UI skeleton for M5 before full PyQt widgets."""

    def __init__(self) -> None:
        self.state = DashboardState()
        self.timeline = EventTimeline(max_events=100)

    def add_event(self, timestamp: float, level: str, message: str) -> None:
        self.timeline.add(timestamp=timestamp, level=level, message=message)

    def render_text(self) -> str:
        events = self.timeline.latest(3)
        events_text = "\n".join([f"[{e.timestamp:>6.1f}] {e.level:<7} {e.message}" for e in events])
        if not events_text:
            events_text = "(no events)"
        return (
            "\n"
            "========== CONVEYOR OPERATOR DASHBOARD ==========\n"
            f"TOTAL COUNT : {self.state.total_count}\n"
            f"UNCERTAIN   : {self.state.uncertain_count}\n"
            f"FPS         : {self.state.fps:.2f}\n"
            f"CAMERA      : {self.state.camera_status}\n"
            f"HEALTH BADGE: {self.state.health_badge()}\n"
            "--------------------------------------------------\n"
            "Recent Events:\n"
            f"{events_text}\n"
            "--------------------------------------------------\n"
            "Controls: [Start] [Stop] [Reset] [Export] [ROI]\n"
            "Tips: Verify CAMERA=HEALTHY and FPS>=35 before shift\n"
            "=================================================="
        )