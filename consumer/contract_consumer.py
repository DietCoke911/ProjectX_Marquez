from datetime import datetime, timezone
from typing import Any, Dict
import json
import os

class ContractConsumer:
    def __init__(self):
        self.decision_log: list = []

    def _log(self, contract_id: str, decision: str, detail: str) -> None:
        ts = datetime.now(timezone.utc).isoformat()
        entry = {
            "timestamp": ts,
            "contract_id": contract_id,
            "decision": decision,
            "detail": detail,
        }
        self.decision_log.append(entry)

        log_path = os.path.expanduser("~/ProjectX_Marquez/audit/consumer.jsonl")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def consume(self, contract: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read-only. Checks version, required fields, and PASS evidence.
        Returns ACCEPT or REFUSE. Does not modify the contract.
        """
        if not isinstance(contract, dict):
            self._log("UNKNOWN", "REFUSE", "Contract is not a dict")
            return {"decision": "REFUSE", "reason": "Contract is not a dict"}

        contract_id = contract.get("contract_id", "UNKNOWN")

        # Required fields
        required = ["contract_id", "contract_version", "scac", "run_date", "gate_results", "confidence"]
        missing = [k for k in required if k not in contract]
        if missing:
            self._log(contract_id, "REFUSE", f"Missing fields: {missing}")
            return {"decision": "REFUSE", "reason": f"Missing fields: {missing}"}

        # Version
        if contract.get("contract_version") != "1.0":
            self._log(contract_id, "REFUSE", f"Incompatible version: {contract.get('contract_version')}")
            return {"decision": "REFUSE", "reason": "Incompatible version"}

        # PASS evidence
        gate_results = contract.get("gate_results", {})
        gate_status = gate_results.get("on_time_rate_gate")
        if gate_status != "PASS":
            self._log(contract_id, "REFUSE", f"Gate not PASS: {gate_status}")
            return {"decision": "REFUSE", "reason": f"Gate not PASS: {gate_status}"}

        # All checks passed
        self._log(contract_id, "ACCEPT", "Version, fields, and PASS evidence verified")
        return {
            "decision": "ACCEPT",
            "contract_id": contract_id,
            "reason": "Version, fields, and PASS evidence verified",
        }

    def get_decision_log(self) -> list:
        return self.decision_log
