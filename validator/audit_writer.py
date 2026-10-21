"""
CMVF Phase 2 Audit Writer — Project x Marquez
Appends every refuse and every successful output path to a single log.
Does not validate. Does not format. Does not execute.
"""

import os
from datetime import datetime, timezone
from typing import Optional

AUDIT_PATH = os.path.expanduser("~/ProjectX_Marquez/audit/chain.log")

class AuditWriter:
    def __init__(self):
        os.makedirs(os.path.dirname(AUDIT_PATH), exist_ok=True)

    def append(self, status: str, detail: str, output_path: Optional[str] = None) -> None:
        """
        Append one line. Status is PASS or REFUSE.
        """
        ts = datetime.now(timezone.utc).isoformat()
        line = f"{ts} | {status} | {detail}"
        if output_path:
            line += f" | {output_path}"
        line += "\n"
        with open(AUDIT_PATH, "a") as f:
            f.write(line)

    def last(self, n: int = 10) -> str:
        """Return the last n lines."""
        if not os.path.exists(AUDIT_PATH):
            return ""
        with open(AUDIT_PATH, "r") as f:
            lines = f.readlines()
        return "".join(lines[-n:])

def main() -> None:
    writer = AuditWriter()
    print(writer.last(20))

if __name__ == "__main__":
    main()

