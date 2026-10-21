"""
CMVF Phase 2 Run Coordinator — Project x Marquez
Sequences gate_runner → validator → writer.
Returns the contract path or None.
Contains no gate logic, no validation logic, and no execution logic.
"""

from typing import Dict, Any, List, Optional
from gate_runner import GateRunner
from cmvf_validator import CMVFValidator
from contract_writer import ContractWriter

class RunCoordinator:
    def __init__(self, scac: str, run_date: str):
        self.scac = scac
        self.run_date = run_date
        self.runner = GateRunner(scac)
        self.validator = CMVFValidator(scac, run_date)
        self.writer = ContractWriter()

    def run(self, raw_rows: List[Dict[str, Any]]) -> Optional[str]:
        """
        Execute the sequence.
        Returns the path to the written contract if every step succeeds.
        Returns None if any step returns empty or fails.
        """
        filtered, metrics = self.runner.prepare_for_validator(raw_rows)
        if not filtered or not metrics:
            return None

        # The validator’s run method still owns the refuse.
        # We pass the already-filtered rows so the validator’s own filter
        # can confirm the same set or fail closed if the sets diverge.
        contract = self.validator.run(filtered)
        if contract is None:
            return None

        path = self.writer.write(contract)
        return path

    def get_audit_log(self) -> list:
        """Return the validator’s audit log after a run."""
        return self.validator.get_audit_log()

