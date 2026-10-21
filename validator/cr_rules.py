"""
CMVF Phase 2 Critical Rule Set — Project x Marquez
Supplies the exact wording required by each critical rule.
Does not format. Does not validate.
"""

from typing import Dict

class CRRules:
    RULES: Dict[str, str] = {
        "CR-01": "No carrier-facing output may be produced without a verified Contract #8.",
        "CR-12": "Every metric shown to the carrier must be present in the contract metrics block.",
        "CR-14": "The disposition line must read READY_FOR_CARRIER_REVIEW or the output is invalid.",
        "CR-15": "The governance note must state that the output was produced from a verified contract and that no self-validation occurred.",
    }

    def get(self, rule_id: str) -> str:
        """Return the required wording for a rule. Return empty string if the rule is unknown."""
        return self.RULES.get(rule_id, "")

    def all_rules(self) -> Dict[str, str]:
        """Return the full set of rules."""
        return dict(self.RULES)

    def required_for_output(self) -> Dict[str, str]:
        """Return only the rules that must appear in every carrier-facing output."""
        return {
            "CR-01": self.RULES["CR-01"],
            "CR-14": self.RULES["CR-14"],
            "CR-15": self.RULES["CR-15"],
        }

