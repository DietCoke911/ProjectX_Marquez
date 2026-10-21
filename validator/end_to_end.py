"""
CMVF Phase 2 End-to-End Runner — Project x Marquez
Takes SCAC, run date, and raw rows path.
Produces a contract and the carrier-facing text in one call.
Refuses at every existing gate.
Logs every refuse and every confirmed output.
"""

import sys
from typing import Optional
from entry_point import load_raw_rows
from run_coordinator import RunCoordinator
from contract_executor import ContractExecutor
from audit_writer import AuditWriter

def run(scac: str, run_date: str, raw_rows_path: str) -> Optional[str]:
    """
    Return the path to the carrier-facing text if every gate passes.
    Return None on any refuse.
    """
    audit = AuditWriter()

    rows = load_raw_rows(raw_rows_path)
    if not rows:
        msg = f"no rows loaded from {raw_rows_path}"
        print(f"REFUSE: {msg}")
        audit.append("REFUSE", msg)
        return None

    coordinator = RunCoordinator(scac, run_date)
    contract_path = coordinator.run(rows)
    if contract_path is None:
        print("REFUSE: coordinator returned None")
        for entry in coordinator.get_audit_log():
            if entry.get("status") != "PASS":
                detail = f"{entry['step']}: {entry['status']} — {entry.get('detail', '')}"
                print(f"  {detail}")
                audit.append("REFUSE", detail)
        audit.append("REFUSE", "coordinator returned None")
        return None

    executor = ContractExecutor()
    output_path = executor.execute(contract_path)
    if output_path is None:
        reason = executor.get_refuse_reason(contract_path)
        print(f"REFUSE: {reason}")
        audit.append("REFUSE", reason)
        return None

    audit.append("PASS", f"output written for {scac} {run_date}", output_path)
    return output_path

def main(scac: str, run_date: str, raw_rows_path: str) -> None:
    result = run(scac, run_date, raw_rows_path)
    if result:
        print(f"OUTPUT_WRITTEN: {result}")
    else:
        print("END_TO_END: refused")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 end_to_end.py <SCAC> <YYYY-MM-DD> <raw_rows.json>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])

