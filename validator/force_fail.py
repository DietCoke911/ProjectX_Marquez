"""
Force one gate failure so the validator writes the REFUSE itself.
"""

from cmvf_validator import CMVFValidator

def main() -> None:
    validator = CMVFValidator(scac="TEST", run_date="2026-10-18")
    # Empty input forces Filter Lock to fail
    result = validator.run(raw_rows=[])
    print("Result:", result)
    print("Audit log entries written to chain.log by the validator.")

if __name__ == "__main__":
    main()

