"""Day 1 dataset audit entry point.

The full audit report is stored in docs/day1_dataset_audit.md.
This script is intentionally a lightweight project marker on Day 1.
Detailed ingestion/validation logic is implemented beginning on Day 2.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
print(f"Project root: {ROOT}")
print(f"Raw data directory: {ROOT / 'data' / 'raw'}")
print("See docs/day1_dataset_audit.md for the audited findings.")
