"""
CMVF Phase 2 Final Verification — Project x Marquez
Confirms that the PASS and REFUSE counts still match the number of
run lines after the CONFIRM, COUNTS, and FINAL lines were appended.
Does not write. Does not validate.
"""

import os
from audit_reader import AuditReader

AUDIT_PATH = os.path.expanduser("~/ProjectX_Marquez/audit/chain.log")
BOUNDARY_PATH = os.path.expanduser("~/ProjectX_Marquez/validator/BOUNDARY.txt")

def main() -> None:
    if not os.path.exists(AUDIT_PATH):
        print("VERIFY_FINAL: log missing")
        return

    with open(AUDIT_PATH, "r") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]

    if not lines:
        print("VERIFY_FINAL: empty log")
        return

    with open(BOUNDARY_PATH, "r") as f:
        boundary = f.read().strip()

    run_lines = 0
    for ln in lines:
        if ln == boundary:
            continue
        if " | CONFIRM | " in ln or " | COUNTS | " in ln or " | FINAL | " in ln:
            continue
        if " | PASS | " in ln or " | REFUSE | " in ln:
            run_lines += 1

    reader = AuditReader()
    counts = reader.count_by_status()

    if counts["PASS"] + counts["REFUSE"] != run_lines:
        print(f"VERIFY_FINAL: mismatch ({counts['PASS'] + counts['REFUSE']} vs {run_lines})")
        return

    print(f"VERIFIED: PASS={counts['PASS']} REFUSE={counts['REFUSE']} runs={run_lines}")

if __name__ == "__main__":
    main()
