"""Structured event logger for pipeline observability."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from typing import Any


class StructuredLogger:
    def __init__(self, module: str) -> None:
        self.module = module
        self._logger = logging.getLogger(module)

    def event(self, name: str, severity: str = "INFO", payload: dict[str, Any] | None = None) -> None:
        message = {
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "module": self.module,
            "event": name,
            "severity": severity,
            "payload": payload or {},
        }
        self._logger.log(getattr(logging, severity.upper(), logging.INFO), json.dumps(message, ensure_ascii=False))