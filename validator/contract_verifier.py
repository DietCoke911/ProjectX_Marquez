"""
CMVF Phase 2 Contract Verifier — Project x Marquez
Verifies any contract file on disk.
Returns True or a refuse reason. Does not write. Does not execute.
"""

import json
import os
from typing import Dict, Any, Optional, Tuple

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

class ContractVerifier:
    def verify_path(self, path: str) -> Tuple[bool, str]:
        """
        Return (True, "") if the contract at path is valid.
        Return (False, reason) otherwise.
        """
        if not os.path.exists(path):
            return False, f"Contract file does not exist: {path}"
        try:
            with open(path, "r") as f:
                contract = json.load(f)
        except Exception as e:
            return False, f"Contract file unreadable: {e}"

        missing = REQUIRED_CONTRACT_FIELDS - set(contract.keys())
        if missing:
            return False, f"Missing required fields: {sorted(missing)}"

        if contract.get("contract_version") != REQUIRED_VERSION:
            return False, f"Wrong contract version: {contract.get('contract_version')}"

        if contract.get("producer") != VALID_PRODUCER:
            return False, f"Invalid producer: {contract.get('producer')}"

        gates = contract.get("gate_results", {})
        if not all(gates.get(g) == "PASS" for g in REQUIRED_GATES):
            return False, "One or more validation gates did not PASS"

        confidence = contract.get("confidence", 0)
        if confidence < 100:
            return False, f"Confidence below 100: {confidence}"

        return True, ""

def main(path: str) -> None:
    verifier = ContractVerifier()
    ok, reason = verifier.verify_path(path)
    if ok:
        print(f"PASS: {path}")
    else:
        print(f"REFUSE: {reason}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 contract_verifier.py <path-to-contract.json>")
        sys.exit(1)
    main(sys.argv[1])

