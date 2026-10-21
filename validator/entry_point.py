"""
CMVF Phase 2 Entry Point — Project x Marquez
Accepts SCAC, run date, and path to raw rows.
Calls the coordinator. Prints the contract path or the refuse reason.
Contains no gate, validation, or execution logic.
"""

import json
import sys
from typing import List, Dict, Any
from run_coordinator import RunCoordinator

def load_raw_rows(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "r") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []

def main(scac: str, run_date: str, raw_rows_path: str) -> None:
    rows = load_raw_rows(raw_rows_path)
    if not rows:
        print(f"REFUSE: no rows loaded from {raw_rows_path}")
        return

    coordinator = RunCoordinator(scac, run_date)
    path = coordinator.run(rows)

    if path:
        print(f"CONTRACT_WRITTEN: {path}")
    else:
        print("REFUSE: coordinator returned None")
        for entry in coordinator.get_audit_log():
            if entry.get("status") != "PASS":
                print(f"  {entry['step']}: {entry['status']} — {entry.get('detail', '')}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python entry_point.py <SCAC> <YYYY-MM-DD> <raw_rows.json>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])

