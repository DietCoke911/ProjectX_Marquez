"""
CMVF Phase 2 Output Formatter — Project x Marquez
Turns a verified contract into carrier-facing text.
Inserts exact CR rule wording from cr_rules.
Does not validate. Does not write contracts.
"""

from typing import Dict, Any, Optional
from cr_rules import CRRules

class OutputFormatter:
    def __init__(self):
        self.rules = CRRules()

    def format(self, contract: Optional[Dict[str, Any]]) -> Optional[str]:
        """
        Return carrier-facing text only if a verified contract is supplied.
        Return None if the contract is None.
        """
        if contract is None:
            return None

        scac = contract.get("scac", "")
        run_date = contract.get("run_date", "")
        contract_id = contract.get("contract_id", "")
        confidence = contract.get("confidence", 0)
        metrics = contract.get("metrics", {})
        row_count = metrics.get("row_count", 0)
        computed_at = metrics.get("computed_at", "")

        required = self.rules.required_for_output()

        lines = [
            f"CMVF Phase 2 Carrier Review — {scac}",
            f"Run Date: {run_date}",
            f"Contract ID: {contract_id}",
            f"Confidence: {confidence}",
            f"Rows Processed: {row_count}",
            f"Computed At: {computed_at}",
            f"Disposition: {required['CR-14'].split('must read ')[1].split(' or')[0]}",
            f"Governance: {required['CR-15']}",
            f"Authority: {required['CR-01']}",
        ]
        return "\n".join(lines)

    def format_to_file(self, contract: Optional[Dict[str, Any]], path: str) -> bool:
        """
        Write the formatted text to path.
        Return True only if the contract was not None and the write succeeded.
        """
        text = self.format(contract)
        if text is None:
            return False
        try:
            with open(path, "w") as f:
                f.write(text)
            return True
        except Exception:
            return False

