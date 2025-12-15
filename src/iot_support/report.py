from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from .analysis import DeviceSummary, snr_voltage_correlation
from .models import LogRecord
from .rules import Finding

def to_markdown(
    device_id: str,
    records: List[LogRecord],
    summary: Optional[DeviceSummary],
    findings: List[Finding],
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines: List[str] = []
    lines.append(f"# IoT Support Report – {device_id}")
    lines.append(f"_Generated: {now}_")
    lines.append("")

    if summary is None:
        lines.append("No records for this device.")
        return "\n".join(lines)

    lines.append("## Summary")
    lines.append(f"- Location: **{summary.location}**")
    lines.append(f"- Data points: **{summary.points}**")
    lines.append(f"- Voltage: min **{summary.min_voltage:.2f}V**, max **{summary.max_voltage:.2f}V**, avg **{summary.avg_voltage:.2f}V**")
    lines.append(f"- SNR: min **{summary.min_snr:.1f} dB**, max **{summary.max_snr:.1f} dB**, avg **{summary.avg_snr:.1f} dB**")
    lines.append(f"- Avg temperature: **{summary.avg_temp:.1f}°C**")
    lines.append(f"- Voltage drop (first→last): **{summary.voltage_drop:.2f}V**")
    lines.append("")

    corr = snr_voltage_correlation(records)
    lines.append("## Signal vs Voltage")
    lines.append(f"- Estimated correlation (SNR ↔ Voltage): **{corr:.2f}** (demo metric)")
    lines.append("")

    lines.append("## Findings")
    for f in findings:
        lines.append(f"### [{f.severity}] {f.title}")
        lines.append(f"- Detail: {f.detail}")
        lines.append(f"- Recommendation: {f.recommendation}")
        lines.append("")

    lines.append("## Raw sample (last 5 records)")
    lines.append("| Timestamp | Voltage (V) | Temp (°C) | SNR (dB) | Status |")
    lines.append("|---|---:|---:|---:|---|")
    for r in records[-5:]:
        lines.append(f"| {r.timestamp} | {r.battery_voltage_v:.2f} | {r.temperature_c:.1f} | {r.signal_snr_db:.1f} | {r.status} |")

    return "\n".join(lines)
