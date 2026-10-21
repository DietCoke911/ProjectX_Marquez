"""
CMVF Phase 2 Gate Runner — Project x Marquez
Supplies filter and calculation logic to the validator.
Returns data only. Does not write contracts. Does not decide gate results.
"""

from typing import Dict, Any, List
from datetime import datetime, timezone

class GateRunner:
    def __init__(self, scac: str):
        self.scac = scac

    def apply_filter_lock(self, raw_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter Lock.
        Returns only rows that meet the CMVF inclusion rules.
        Empty result is a valid return; the validator treats it as a fail-closed condition.
        """
        if not raw_rows:
            return []
        # Real CMVF filter rules replace the condition below.
        # Current rule: keep rows that contain a non-empty ISA identifier and a valid SCAC match.
        filtered = [
            row for row in raw_rows
            if row.get("isa") and row.get("scac") == self.scac
        ]
        return filtered

    def run_calculation_engine(self, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculation Engine.
        Computes metrics from the filtered rows only.
        Returns the metrics dict. Does not score confidence or write a contract.
        """
        if not rows:
            return {}
        # Real CMVF metric calculations replace the structure below.
        # Current metrics are derived only from the rows that survived the filter.
        metrics = {
            "row_count": len(rows),
            "unique_isas": len({row.get("isa") for row in rows if row.get("isa")}),
            "computed_at": datetime.now(timezone.utc).isoformat(),
            "scac": self.scac,
        }
        return metrics

    def prepare_for_validator(self, raw_rows: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], Dict[str, Any]]:
        """
        Convenience method that runs filter then calculation.
        Returns (filtered_rows, metrics). The validator decides whether either result is acceptable.
        """
        filtered = self.apply_filter_lock(raw_rows)
        metrics = self.run_calculation_engine(filtered)
        return filtered, metrics

