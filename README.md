# IoT Support Assistant

Small project that analyzes IoT gateway logs (CSV) and produces:
- anomaly detection (weak signal, voltage sag),
- rule-based recommendations,
- markdown report for support & customers.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]

iot-support analyze sample_data/chester_logs.csv --device CHESTER-GW-02 --out report.md
