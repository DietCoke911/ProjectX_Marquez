"""
CMVF Phase 2 Contract Writer — Project x Marquez
Persists the contract object returned by the validator.
Writes only. Does not validate. Does not execute. Does not read the file after writing.
"""

import json
import os
from typing import Dict, Any, Optional

CONTRACT_DIR = os.path.expanduser("~/ProjectX_Marquez/contracts")
FILENAME_PATTERN = "CMVF-{scac}-{run_date}.json"

class ContractWriter:
    def __init__(self, contract_dir: str = CONTRACT_DIR):
        self.contract_dir = contract_dir
        os.makedirs(self.contract_dir, exist_ok=True)

    def write(self, contract: Optional[Dict[str, Any]]) -> Optional[str]:
        """
        Write the contract to disk.
        Returns the full path if the write succeeds.
        Returns None if the contract is None or the write fails.
        Does not read the file after writing.
        """
        if contract is None:
            return None
        scac = contract.get("scac")
        run_date = contract.get("run_date")
        if not scac or not run_date:
            return None
        filename = FILENAME_PATTERN.format(scac=scac, run_date=run_date)
        path = os.path.join(self.contract_dir, filename)
        try:
            with open(path, "w") as f:
                json.dump(contract, f, indent=2)
            return path
        except Exception:
            return None

    def path_for(self, scac: str, run_date: str) -> str:
        """Return the path the consumer will use for a given SCAC and run date."""
        filename = FILENAME_PATTERN.format(scac=scac, run_date=run_date)
        return os.path.join(self.contract_dir, filename)
