"""
CMVF Phase 2 Contract Consumer — Project x Marquez
Reads only. Never writes a contract. Never calls the validator.
Refuses if the contract is missing, incomplete, or not produced by CMVFValidator.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, Optional

REQUIRED_CONTRACT_FIELDS = {
    "contract_id",
    "contract_version",
    "scac",
    "run_date",
    "metrics",
    "gate_results",
    "confidence",
    "timestamp",
    "producer",
}
REQUIRED_GATES = ["V-01", "V-02", "V-03", "V-04", "V-05"]
VALID_PRODUCER = "CMVFValidator"
REQUIRED_VERSION = "2.0"

class ContractConsumer:
    def __init__(self, contract_path: str):
        self.contract_path = contract_path
        self.contract: Optional[Dict[str, Any]] = None
        self.refused = False
        self.refuse_reason = ""

    def _refuse(self, reason: str) -> None:
        self.refused = True
        self.refuse_reason = reason

    def load(self) -> bool:
        """Load the contract from disk. Refuse if the file is missing or unreadable."""
        if not os.path.exists(self.contract_path):
            self._refuse(f"Contract file does not exist: {self.contract_path}")
            return False
        try:
            with open(self.contract_path, "r") as f:
                self.contract = json.load(f)
        except Exception as e:
            self._refuse(f"Contract file unreadable: {e}")
            return False
        return True

    def verify(self) -> bool:
        """Verify the contract meets the Phase 2 contract. Refuse on any failure."""
        if self.refused or not self.contract:
            return False

        missing = REQUIRED_CONTRACT_FIELDS - set(self.contract.keys())
        if missing:
            self._refuse(f"Missing required fields: {sorted(missing)}")
            return False

        if self.contract.get("contract_version") != REQUIRED_VERSION:
            self._refuse(f"Wrong contract version: {self.contract.get('contract_version')}")
            return False

        if self.contract.get("producer") != VALID_PRODUCER:
            self._refuse(f"Invalid producer: {self.contract.get('producer')}")
            return False

        gates = self.contract.get("gate_results", {})
        if not all(gates.get(g) == "PASS" for g in REQUIRED_GATES):
            self._refuse("One or more validation gates did not PASS")
            return False

        confidence = self.contract.get("confidence", 0)
        if confidence < 100:
            self._refuse(f"Confidence below 100: {confidence}")
            return False

        return True

    def consume(self) -> Optional[Dict[str, Any]]:
        """Return the contract only if load and verify both succeed. Otherwise None."""
        if not self.load():
            return None
        if not self.verify():
            return None
        return self.contract

    def get_refuse_reason(self) -> str:
        return self.refuse_reason if self.refused else ""

