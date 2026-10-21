"""
CMVF Phase 2 Contract Executor — Project x Marquez
Calls the consumer. If the consumer returns a contract, formats it
and writes the carrier-facing text. Refuses if the consumer returns None.
"""

import os
from typing import Optional, Dict, Any
from contract_consumer import ContractConsumer
from output_formatter import OutputFormatter

OUTPUT_DIR = os.path.expanduser("~/ProjectX_Marquez/outputs")

class ContractExecutor:
    def __init__(self):
        self.formatter = OutputFormatter()
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def execute(self, contract_path: str) -> Optional[str]:
        """
        Return the path to the written output file if the contract is valid.
        Return None if the consumer refuses.
        """
        consumer = ContractConsumer(contract_path)
        contract = consumer.consume()
        if contract is None:
            return None

        output_name = f"{contract.get('contract_id', 'UNKNOWN')}.txt"
        output_path = os.path.join(OUTPUT_DIR, output_name)

        wrote = self.formatter.format_to_file(contract, output_path)
        return output_path if wrote else None

    def get_refuse_reason(self, contract_path: str) -> str:
        """
        Return the consumer's refuse reason.
        """
        consumer = ContractConsumer(contract_path)
        return consumer.get_refuse_reason() or "Consumer refused the contract"

def main(path: str) -> None:
    executor = ContractExecutor()
    result = executor.execute(path)
    if result:
        print(f"OUTPUT_WRITTEN: {result}")
    else:
        print(f"REFUSE: {executor.get_refuse_reason(path)}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 contract_executor.py <path-to-contract.json>")
        sys.exit(1)
    main(sys.argv[1])
