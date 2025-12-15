from __future__ import annotations
import csv
from datetime import datetime
from pathlib import Path
from typing import Iterable, List

from .models import LogRecord

_TS_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
]

def _parse_ts(value: str) -> datetime:
    value = value.strip()
    for fmt in _TS_FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unsupported timestamp format: {value}")

def read_csv(path: str | Path) -> List[LogRecord]:
    path = Path(path)
    records: List[LogRecord] = []

    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {
            "Timestamp","Device_ID","Location","Battery_Voltage_V",
            "Temperature_C","Signal_SNR_dB","Send_Interval_Min","Status"
        }
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(f"CSV missing required columns. Found: {reader.fieldnames}")

        for row in reader:
            records.append(
                LogRecord(
                    timestamp=_parse_ts(row["Timestamp"]),
                    device_id=row["Device_ID"].strip(),
                    location=row["Location"].strip(),
                    battery_voltage_v=float(row["Battery_Voltage_V"]),
                    temperature_c=float(row["Temperature_C"]),
                    signal_snr_db=float(row["Signal_SNR_dB"]),
                    send_interval_min=int(row["Send_Interval_Min"]),
                    status=row["Status"].strip(),
                )
            )

    records.sort(key=lambda r: r.timestamp)
    return records

def filter_device(records: Iterable[LogRecord], device_id: str) -> List[LogRecord]:
    did = device_id.strip()
    out = [r for r in records if r.device_id == did]
    out.sort(key=lambda r: r.timestamp)
    return out
