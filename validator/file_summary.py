"""
CMVF Phase 2 File Summary — Project x Marquez
Lists every .py file in the validator directory with a one-line purpose.
Does not execute. Does not validate.
"""

import os

PURPOSES = {
    "entry_point.py": "Loads raw rows from a JSON path.",
    "run_coordinator.py": "Coordinates the run and produces a contract path or None.",
    "contract_consumer.py": "Verifies a contract and returns it or refuses.",
    "output_formatter.py": "Formats a verified contract into carrier-facing text.",
    "contract_executor.py": "Calls the consumer and writes the formatted text.",
    "end_to_end.py": "Runs the full chain from raw rows to output or refuse.",
    "audit_writer.py": "Appends PASS and REFUSE lines to the audit log.",
    "audit_reader.py": "Returns the last N audit entries as structured records.",
    "status_report.py": "Prints a one-line summary of the last run and counts.",
    "confirm_chain.py": "Writes known-good rows and confirms the full chain.",
    "refuse_test.py": "Feeds known-bad rows and confirms refuse is logged.",
    "file_summary.py": "Lists every module and its one-line purpose.",
    "cmvf_validator.py": "Earlier validator retained for reference.",
    "contract_verifier.py": "Earlier verifier retained for reference.",
    "contract_writer.py": "Earlier writer retained for reference.",
    "cr_rules.py": "Holds the CR rule strings that appear in every output.",
    "gate_runner.py": "Earlier gate runner retained for reference.",
    "test_harness.py": "Earlier harness retained for reference.",
}

def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    files = sorted(f for f in os.listdir(here) if f.endswith(".py"))
    print(f"VALIDATOR MODULES ({len(files)})")
    for name in files:
        purpose = PURPOSES.get(name, "—")
        print(f"  {name:<24} {purpose}")

if __name__ == "__main__":
    main()
