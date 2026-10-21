"""
CMVF Phase 2 Audit Reader — Project x Marquez
Returns the last N lines of the audit log as structured records.
Skips the boundary header if present.
Treats CONFIRM, COUNTS, FINAL, VERIFIED, VERIFIED_CONFIRM,
VERIFIED_CONFIRM_CONFIRM, and VERIFIED_CONFIRM_CONFIRM_CONFIRM lines
as neither PASS nor REFUSE.
Accepts lines with or without an output path.
Does not write. Does not validate.
"""

import os
from typing import List, Dict

AUDIT_PATH = os.path.expanduser("~/ProjectX_Marquez/audit/chain.log")
BOUNDARY_PATH = os.path.expanduser("~/ProjectX_Marquez/validator/BOUNDARY.txt")

class AuditReader:
    def __init__(self, path: str = AUDIT_PATH) -> None:
        self.path = path
        self.boundary = self._load_boundary()

    def _load_boundary(self) -> str:
        if not os.path.exists(BOUNDARY_PATH):
            return ""
        with open(BOUNDARY_PATH, "r") as f:
            return f.read().strip()

    def last(self, n: int = 10) -> List[Dict[str, str]]:
        if not os.path.exists(self.path):
            return []
        with open(self.path, "r") as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]
        if lines and lines[0] == self.boundary:
            lines = lines[1:]
        records = []
        for ln in lines[-n:]:
            parts = ln.split(" | ")
            if len(parts) >= 3:
                records.append({
                    "ts": parts[0],
                    "status": parts[1],
                    "detail": parts[2],
                    "output_path": parts[3] if len(parts) > 3 else "",
                })
        return records

    def count_by_status(self) -> Dict[str, int]:
        if not os.path.exists(self.path):
            return {"PASS": 0, "REFUSE": 0}
        with open(self.path, "r") as f:
            lines = [ln.strip() for ln in f.readlines() if ln.strip()]
        if lines and lines[0] == self.boundary:
            lines = lines[1:]
        counts = {"PASS": 0, "REFUSE": 0}
        for ln in lines:
            if " | PASS | " in ln:
                counts["PASS"] += 1
            elif " | REFUSE | " in ln:
                counts["REFUSE"] += 1
        return counts
