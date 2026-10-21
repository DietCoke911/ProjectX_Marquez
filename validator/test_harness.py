"""
CMVF Phase 2 Test Harness — Project x Marquez
Runs one known-good case and one known-bad case.
Asserts path on good, refuse on bad.
Contains no production logic.
"""

import json
import os
import tempfile
from entry_point import load_raw_rows
from run_coordinator import RunCoordinator

def write_temp_rows(rows: list) -> str:
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(rows, f)
    return path

def run_case(label: str, rows: list, scac: str, run_date: str, expect_path: bool) -> bool:
    path = write_temp_rows(rows)
    coordinator = RunCoordinator(scac, run_date)
    result = coordinator.run(rows)
    os.unlink(path)

    if expect_path and result:
        print(f"PASS {label}: contract written to {result}")
        return True
    if not expect_path and result is None:
        print(f"PASS {label}: refuse as expected")
        return True
    print(f"FAIL {label}: expected {'path' if expect_path else 'refuse'}, got {result}")
    return False

def main() -> None:
    scac = "TEST"
    run_date = "2026-10-17"

    good_rows = [
        {"isa": "ISA001", "scac": "TEST", "value": 100},
        {"isa": "ISA002", "scac": "TEST", "value": 200},
    ]
    bad_rows = [
        {"isa": "", "scac": "OTHER", "value": 0},
    ]

    ok1 = run_case("known-good", good_rows, scac, run_date, expect_path=True)
    ok2 = run_case("known-bad", bad_rows, scac, run_date, expect_path=False)

    if ok1 and ok2:
        print("HARNESS: all assertions passed")
    else:
        print("HARNESS: one or more assertions failed")

if __name__ == "__main__":
    main()

