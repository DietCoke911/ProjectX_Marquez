"""
CMVF Phase 2 — New Refuse Test
Uses AuditWriter to append one new REFUSE that is not already in the log.
"""

import os
from audit_writer import AuditWriter

AUDIT_PATH = os.path.expanduser("~/ProjectX_Marquez/audit/chain.log")

def main() -> None:
    writer = AuditWriter()

    # One new case that should be refused
    writer.append(
        status="REFUSE",
        detail="NEW_TEST: single option and confidence 0.3 — rules not met"
    )

    print("New REFUSE appended.")
    print()
    print(writer.last(5))

if __name__ == "__main__":
    main()
