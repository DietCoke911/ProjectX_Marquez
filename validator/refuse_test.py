"""
CMVF Phase 2 Refuse Test — Project x Marquez
Feeds a known-bad raw-rows file.
Confirms the chain refuses and that the refuse is written to the audit log.
"""

import json
import os
import tempfile
from end_to_end import run
from audit_reader import AuditReader

def main() -> None:
    scac = "BAD"
    run_date = "2026-10-17"

    # Known-bad: empty list
    rows = []

    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w") as f:
        json.dump(rows, f)

    print(f"RAW_ROWS: {path}")
    result = run(scac, run_date, path)
    os.unlink(path)

    if result is not None:
        print("REFUSE_TEST_FAILED: chain returned a path on bad input")
        return

    reader = AuditReader()
    last = reader.last(1)
    if not last or last[0]["status"] != "REFUSE":
        print("REFUSE_TEST_FAILED: no REFUSE entry written")
        return

    print("REFUSE_CONFIRMED")
    print(last[0])

if __name__ == "__main__":
    main()

