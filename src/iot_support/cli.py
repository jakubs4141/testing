from __future__ import annotations
import argparse
from pathlib import Path

from .parser import read_csv, filter_device
from .analysis import summarize_device
from .rules import evaluate
from .report import to_markdown

def main() -> None:
    parser = argparse.ArgumentParser(prog="iot-support")
    sub = parser.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze", help="Analyze CSV log and generate report")
    a.add_argument("csv_path", type=str)
    a.add_argument("--device", required=True, type=str)
    a.add_argument("--out", default="report.md", type=str)

    args = parser.parse_args()

    if args.cmd == "analyze":
        records = read_csv(args.csv_path)
        dev_records = filter_device(records, args.device)

        summary = summarize_device(dev_records)
        findings = evaluate(dev_records)
        md = to_markdown(args.device, dev_records, summary, findings)

        out = Path(args.out)
        out.write_text(md, encoding="utf-8")
        print(f"OK: report written to {out.resolve()}")

if __name__ == "__main__":
    main()
