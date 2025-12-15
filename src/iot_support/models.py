from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class LogRecord:
    timestamp: datetime
    device_id: str
    location: str
    battery_voltage_v: float
    temperature_c: float
    signal_snr_db: float
    send_interval_min: int
    status: str
