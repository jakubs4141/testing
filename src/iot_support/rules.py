from __future__ import annotations
from dataclasses import dataclass
from typing import List

from .models import LogRecord

@dataclass(frozen=True)
class Finding:
    severity: str  # INFO/WARN/ERROR
    title: str
    detail: str
    recommendation: str

def evaluate(records: List[LogRecord]) -> List[Finding]:
    if not records:
        return [Finding("INFO", "No data", "No records provided.", "Provide device logs.")]

    findings: List[Finding] = []

    cold = any(r.temperature_c < 15 for r in records)
    weak_snr = any(r.signal_snr_db < -10 for r in records)
    very_weak_snr = any(r.signal_snr_db < -15 for r in records)
    low_voltage = any(r.battery_voltage_v < 3.5 for r in records)

    retry_like = any("RETRY" in r.status.upper() for r in records)
    packet_loss = any("PACKETLOSS" in r.status.upper() for r in records)

    if weak_snr:
        findings.append(Finding(
            "WARN",
            "Weak signal detected",
            "Signal SNR frequently drops below -10 dB.",
            "Consider moving gateway/antenna or increasing send interval to reduce retries and battery stress."
        ))

    if cold and weak_snr:
        findings.append(Finding(
            "WARN",
            "Cold + weak signal = voltage sag risk",
            "Temperature is < 15°C and SNR is poor. This increases voltage sag during transmissions.",
            "Increase send interval (e.g., 60 min) and avoid immediate retries under bad SNR."
        ))

    if retry_like and very_weak_snr:
        findings.append(Finding(
            "ERROR",
            "Aggressive retries under very weak SNR",
            "Device retries connection while SNR is < -15 dB, wasting energy and likely increasing packet loss.",
            "Disable immediate retries; implement backoff and longer interval when SNR is poor."
        ))

    if low_voltage and cold:
        findings.append(Finding(
            "WARN",
            "Low voltage under cold conditions",
            "Voltage dips below 3.5V while temperature is low; this might be a false low-battery alarm (voltage sag).",
            "Correlate with transmissions; allow recovery time; verify battery health after changing retry/interval behavior."
        ))

    if packet_loss:
        findings.append(Finding(
            "WARN",
            "Packet loss reported",
            "Log indicates ERROR_PacketLoss events.",
            "Check gateway placement, interference, and LoRaWAN settings (SF, power, ADR)."
        ))

    if not findings:
        findings.append(Finding(
            "INFO",
            "No major anomalies",
            "No obvious risky patterns detected in the provided window.",
            "Monitor longer timeframe or collect more frequent diagnostics."
        ))

    return findings
