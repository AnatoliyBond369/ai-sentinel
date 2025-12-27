# core/schema.py

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class SensorSignal:
    sensor: str
    status: str
    timestamp: str
    data: Dict[str, Any]
    message: Optional[str] = None

    @staticmethod
    def now_utc() -> str:
        """Текущее время UTC (timezone-aware, Python 3.12+)"""
        return datetime.now(timezone.utc).isoformat()
