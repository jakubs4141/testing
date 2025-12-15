from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Optional

from .models import LogRecord

@dataclass(frozen=True)
class DeviceSummary:
    device_id: str
    location: str
    min_voltage: float
    max_voltage: float
    avg_voltage: float
    min_snr: float
    max_snr: float
    avg_snr: float
    avg_temp: float
    points: int
    voltage_drop: float  # first - last (positive means drop)

def _avg(values: List[float]) -> float:
    return sum(values) / len(values) if values else 0.0

def summarize_device(records: Iterable[LogRecord]) -> Optional[DeviceSummary]:
    recs = list(records)
    if not recs:
        return None

    volts = [r.battery_voltage_v for r in recs]
    snrs = [r.signal_snr_db for r in recs]
    temps = [r.temperature_c for r in recs]

    return DeviceSummary(
        device_id=recs[0].device_id,
        location=recs[0].location,
        min_voltage=min(volts),
        max_voltage=max(volts),
        avg_voltage=_avg(volts),
        min_snr=min(snrs),
        max_snr=max(snrs),
        avg_snr=_avg(snrs),
        avg_temp=_avg(temps),
        points=len(recs),
        voltage_drop=(volts[0] - volts[-1]),
    )

def simple_correlation(xs: List[float], ys: List[float]) -> float:
    """
    Pearson correlation without numpy.
    Returns value in [-1, 1]. If not enough variance, returns 0.
    """
    if len(xs) != len(ys) or len(xs) < 2:
        return 0.0

    mx = sum(xs) / len(xs)
    my = sum(ys) / len(ys)

    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = sum((x - mx) ** 2 for x in xs)
    deny = sum((y - my) ** 2 for y in ys)

    if denx == 0 or deny == 0:
        return 0.0

    return num / ((denx * deny) ** 0.5)

def snr_voltage_correlation(records: List[LogRecord]) -> float:
    snr = [r.signal_snr_db for r in records]
    v = [r.battery_voltage_v for r in records]
    return simple_correlation(snr, v)
